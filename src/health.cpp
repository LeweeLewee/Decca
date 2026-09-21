#include "health.h"
#if DECCA_HEALTH_ENABLED
#include "health_model.h"
#include "version.h"
#include <Arduino.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <esp_system.h>
#include <esp_timer.h>
#include <mqtt_client.h>
#include <atomic>
#include <cstring>

#if __has_include("secrets.h")
#include "secrets.h"
#endif
#ifndef DECCA_HEALTH_BROKER
#define DECCA_HEALTH_BROKER ""
#endif
#ifndef DECCA_HEALTH_USER
#define DECCA_HEALTH_USER ""
#endif
#ifndef DECCA_HEALTH_PASSWORD
#define DECCA_HEALTH_PASSWORD ""
#endif
#ifndef DECCA_HEALTH_INTERVAL_MS
#define DECCA_HEALTH_INTERVAL_MS 300000UL
#endif
static_assert(DECCA_HEALTH_INTERVAL_MS >= 300000UL &&
              DECCA_HEALTH_INTERVAL_MS <= 1800000UL,
              "Trial reporting interval must be 5 to 30 minutes");

namespace decca::health {
namespace {
constexpr char kStateTopic[] = "decca/trial/health/state";
constexpr char kAvailabilityTopic[] = "decca/trial/health/availability";
constexpr uint32_t kInterval = DECCA_HEALTH_INTERVAL_MS;
constexpr uint32_t kWarmupMs = 60000;
portMUX_TYPE g_mux = portMUX_INITIALIZER_UNLOCKED;
Aggregator g_aggregate;
bool g_active = false;
bool g_powerOn = false;
bool g_vinyl = false;
char g_wiimStatus[24] = "disabled";
uint32_t g_lastSampleMs = 0;
uint32_t g_lastLoopUs = 0;
bool g_loopSeen = false;
std::atomic<bool> g_connected{false};
std::atomic<uint32_t> g_mqttDisconnects{0};
esp_mqtt_client_handle_t g_client = nullptr;
TaskHandle_t g_worker = nullptr;

void mqttEvent(void*, esp_event_base_t, int32_t id, void*) {
    if (id == MQTT_EVENT_CONNECTED) g_connected.store(true);
    if (id == MQTT_EVENT_DISCONNECTED) {
        if (g_connected.exchange(false)) ++g_mqttDisconnects;
    }
}
const char* resetReason() {
    switch (esp_reset_reason()) {
        case ESP_RST_POWERON: return "power_on";
        case ESP_RST_SW: return "software";
        case ESP_RST_PANIC: return "panic";
        case ESP_RST_INT_WDT: return "interrupt_watchdog";
        case ESP_RST_TASK_WDT: return "task_watchdog";
        case ESP_RST_WDT: return "watchdog";
        case ESP_RST_BROWNOUT: return "brownout";
        case ESP_RST_DEEPSLEEP: return "deep_sleep";
        case ESP_RST_EXT: return "external";
        default: return "unknown";
    }
}
bool publishSummary() {
    Window window;
    Counters counters;
    bool on, vinyl;
    char wiimStatus[24];
    portENTER_CRITICAL(&g_mux);
    window = g_aggregate.take();
    counters = g_aggregate.counters;
    on = g_powerOn;
    vinyl = g_vinyl;
    std::memcpy(wiimStatus, g_wiimStatus, sizeof(wiimStatus));
    portEXIT_CRITICAL(&g_mux);

    StaticJsonDocument<1024> json;
    json["schema"] = 1;
    json["firmware"] = version::kFirmwareVersion;
    json["uptime_s"] = static_cast<uint64_t>(esp_timer_get_time() / 1000000);
    json["reset_reason"] = resetReason();
    json["free_heap_b"] = ESP.getFreeHeap();
    json["min_heap_b"] = ESP.getMinFreeHeap();
    const bool wifi = WiFi.status() == WL_CONNECTED;
    if (wifi) json["rssi_dbm"] = WiFi.RSSI();
    else json["rssi_dbm"] = nullptr;
    if (window.hasRssi) json["min_rssi_dbm"] = window.minRssi;
    else json["min_rssi_dbm"] = nullptr;
    json["wifi_disconnects"] = counters.wifiDisconnects;
    json["wiim_faults"] = counters.wiimFaults;
    json["mqtt_disconnects"] = g_mqttDisconnects.load();
    json["max_loop_gap_us"] = window.maxLoopGapUs;
    json["samples"] = window.samples;
    json["interval_s"] = kInterval / 1000;
    json["power"] = on ? "on" : "standby";
    json["source"] = vinyl ? "vinyl" : "digital";
    json["wiim_status"] = wiimStatus;
    char payload[1024];
    bool sent = false;
    if (!json.overflowed() && measureJson(json) < sizeof(payload)) {
        const size_t length = serializeJson(json, payload, sizeof(payload));
        // QoS 0 and non-retained: no outbox/backlog, no replay of stale health.
        sent = esp_mqtt_client_publish(g_client, kStateTopic, payload,
                                      length, 0, 0) >= 0;
    }
    if (!sent) {
        portENTER_CRITICAL(&g_mux);
        g_aggregate.restore(window);
        portEXIT_CRITICAL(&g_mux);
    }
    return sent;
}
void worker(void*) {
    // Avoid network/task allocation competing with boot and initial WiiM setup.
    vTaskDelay(pdMS_TO_TICKS(kWarmupMs));
    esp_mqtt_client_config_t config{};
    config.host = DECCA_HEALTH_BROKER;
    config.port = 1883;
    config.transport = MQTT_TRANSPORT_OVER_TCP;
    config.client_id = "decca-health-trial";
    config.username = DECCA_HEALTH_USER;
    config.password = DECCA_HEALTH_PASSWORD;
    config.lwt_topic = kAvailabilityTopic;
    config.lwt_msg = "offline";
    config.lwt_qos = 0;
    config.lwt_retain = 1;
    config.keepalive = 120;
    config.task_prio = 1;
    config.task_stack = 4096;
    config.buffer_size = 1280;
    config.reconnect_timeout_ms = kInterval;
    config.network_timeout_ms = 1000;
    config.protocol_ver = MQTT_PROTOCOL_V_3_1_1;
    g_client = esp_mqtt_client_init(&config);
    if (!g_client) { vTaskDelete(nullptr); return; }
    if (esp_mqtt_client_register_event(g_client, MQTT_EVENT_ANY, mqttEvent,
                                       nullptr) != ESP_OK ||
        esp_mqtt_client_start(g_client) != ESP_OK) {
        esp_mqtt_client_destroy(g_client);
        g_client = nullptr;
        vTaskDelete(nullptr);
        return;
    }
    // Every attempt is rate limited, including failures and reconnects.
    uint32_t lastAttempt = millis() - kInterval;
    for (;;) {
        const uint32_t now = millis();
        if (g_connected.load() && due(now, lastAttempt, kInterval)) {
            lastAttempt = now;
            if (publishSummary()) {
                esp_mqtt_client_publish(g_client, kAvailabilityTopic,
                                        "online", 0, 0, 1);
            }
        }
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
}  // namespace

void init() {
    // Trial uses a numeric LAN IPv4 address, avoiding DNS work/retries.
    IPAddress broker;
    if (!broker.fromString(DECCA_HEALTH_BROKER) ||
        std::strlen(DECCA_HEALTH_USER) == 0 ||
        std::strlen(DECCA_HEALTH_PASSWORD) == 0) return;
    if (xTaskCreatePinnedToCore(worker, "health", 6144, nullptr, 1,
                               &g_worker, 0) != pdPASS) return;
    WiFi.onEvent([](WiFiEvent_t event) {
        if (event != ARDUINO_EVENT_WIFI_STA_GOT_IP &&
            event != ARDUINO_EVENT_WIFI_STA_DISCONNECTED) return;
        portENTER_CRITICAL(&g_mux);
        g_aggregate.wifi(event == ARDUINO_EVENT_WIFI_STA_GOT_IP);
        portEXIT_CRITICAL(&g_mux);
    });
    const bool connected = WiFi.status() == WL_CONNECTED;
    portENTER_CRITICAL(&g_mux);
    g_aggregate.wifi(connected);
    portEXIT_CRITICAL(&g_mux);
    g_active = true;
}
void update(const Inputs& inputs) {
    if (!g_active) return;
    const uint32_t nowUs = micros();
    const uint32_t nowMs = millis();
    const bool sample = due(nowMs, g_lastSampleMs, 1000);
    const bool connected = sample && WiFi.status() == WL_CONNECTED;
    const int32_t rssi = connected ? WiFi.RSSI() : 0;
    portENTER_CRITICAL(&g_mux);
    if (g_loopSeen) g_aggregate.loopGap(nowUs - g_lastLoopUs);
    g_aggregate.wiim(inputs.wiimFault);
    g_powerOn = inputs.powerOn;
    g_vinyl = inputs.vinyl;
    std::strncpy(g_wiimStatus, inputs.wiimStatus, sizeof(g_wiimStatus) - 1);
    g_wiimStatus[sizeof(g_wiimStatus) - 1] = '\0';
    if (sample) g_aggregate.sample(connected, rssi);
    portEXIT_CRITICAL(&g_mux);
    g_loopSeen = true;
    g_lastLoopUs = nowUs;
    if (sample) g_lastSampleMs = nowMs;
}
}  // namespace decca::health
#else
namespace decca::health {
void init() {}
void update(const Inputs&) {}
}
#endif

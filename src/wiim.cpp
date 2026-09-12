#include "wiim.h"

#include <Arduino.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <cstring>

#if __has_include("secrets.h")
#include "secrets.h"
#endif
#ifndef DECCA_WIIM_HOST
#define DECCA_WIIM_HOST ""
#endif

namespace decca::wiim {
namespace {

#ifndef PIO_UNIT_TESTING
constexpr char kPlayerStatusCommand[] = "getPlayerStatus";
constexpr char kMetadataCommand[] = "getMetaInfo";
constexpr uint32_t kWorkerDelayMs = 25;
constexpr uint32_t kRetryIntervalMs = 2000;
constexpr uint8_t kFailureThreshold = 3;
constexpr uint8_t kWorkerCore = 0;
// HTTPS requests, the response buffer and ArduinoJson parsing overlap on this
// task's stack.  Eight KiB resets the installed ESP32 during the first live
// request, so retain explicit headroom for the TLS/HTTP call chain.
constexpr uint16_t kWorkerStackBytes = 16384;
#endif

Snapshot g_publicSnapshot;
Snapshot g_sharedSnapshot;
Snapshot g_workerSnapshot;
portMUX_TYPE g_mux = portMUX_INITIALIZER_UNLOCKED;
#ifndef PIO_UNIT_TESTING
TaskHandle_t g_task = nullptr;
#endif
settings::Source g_requestedSource = settings::Source::DigitalStreamer;
uint8_t g_requestedVolume = 0;
bool g_sourceDirty = true;
bool g_volumeDirty = true;
bool g_requestedPowerOn = false;
bool g_powerDirty = true;

bool hasText(const char* value) {
    return value != nullptr && value[0] != '\0';
}

template <size_t Capacity>
void copyText(char (&destination)[Capacity], const char* source) {
    std::strncpy(destination, source == nullptr ? "" : source, Capacity - 1U);
    destination[Capacity - 1U] = '\0';
}

bool isHexText(const char* value) {
    if (!hasText(value)) {
        return false;
    }
    const size_t length = std::strlen(value);
    if ((length % 2U) != 0U) {
        return false;
    }
    for (size_t i = 0; i < length; ++i) {
        const char c = value[i];
        if (!((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') ||
              (c >= 'A' && c <= 'F'))) {
            return false;
        }
    }
    return true;
}

uint8_t hexNibble(char value) {
    if (value >= '0' && value <= '9') return value - '0';
    if (value >= 'a' && value <= 'f') return value - 'a' + 10U;
    return value - 'A' + 10U;
}

template <size_t Capacity>
void copyPossiblyHexText(char (&destination)[Capacity], const char* source) {
    if (!isHexText(source)) {
        copyText(destination, source);
        return;
    }
    const size_t sourceLength = std::strlen(source);
    const size_t outputLength =
        min((sourceLength / 2U), static_cast<size_t>(Capacity - 1U));
    for (size_t i = 0; i < outputLength; ++i) {
        destination[i] = static_cast<char>((hexNibble(source[i * 2U]) << 4U) |
                                           hexNibble(source[i * 2U + 1U]));
    }
    destination[outputLength] = '\0';
}

Playback playbackFrom(const char* value) {
    if (value == nullptr) return Playback::None;
    if (std::strcmp(value, "play") == 0) return Playback::Playing;
    if (std::strcmp(value, "pause") == 0) return Playback::Paused;
    if (std::strcmp(value, "loading") == 0) return Playback::Loading;
    if (std::strcmp(value, "stop") == 0) return Playback::Stopped;
    return Playback::None;
}

bool parsePlayer(const char* json, Snapshot& output) {
    if (!hasText(json)) return false;
    StaticJsonDocument<1536> document;
    if (deserializeJson(document, json) != DeserializationError::Ok) return false;

    output.mode = document["mode"].isNull() ? -1 : document["mode"].as<int>();
    output.volume = constrain(document["vol"].as<int>(), 0, 100);
    output.muted = document["mute"].as<int>() != 0;
    output.playback = playbackFrom(document["status"] | "");

    if (output.playback == Playback::None ||
        output.playback == Playback::Stopped) {
        output.title[0] = '\0';
        output.artist[0] = '\0';
        output.metadataValid = false;
    }

    const char* title = document["Title"] | "";
    const char* artist = document["Artist"] | "";
    if (hasText(title) && std::strcmp(title, "556E6B6E6F776E") != 0) {
        copyPossiblyHexText(output.title, title);
    }
    if (hasText(artist) && std::strcmp(artist, "556E6B6E6F776E") != 0) {
        copyPossiblyHexText(output.artist, artist);
    }
    output.metadataValid = hasText(output.title) || hasText(output.artist);
    return true;
}

bool parseMeta(const char* json, Snapshot& output) {
    if (!hasText(json)) return false;
    StaticJsonDocument<2304> document;
    if (deserializeJson(document, json) != DeserializationError::Ok) return false;
    JsonVariantConst metadata = document["metaData"];
    if (metadata.isNull()) return false;
    copyText(output.title, metadata["title"] | "");
    copyText(output.artist, metadata["artist"] | "");
    output.metadataValid = hasText(output.title) || hasText(output.artist);
    return true;
}

const char* commandForSource(settings::Source source) {
    return source == settings::Source::Vinyl
               ? "setPlayerCmd:switchmode:line-in"
               : "setPlayerCmd:switchmode:wifi";
}

#ifndef PIO_UNIT_TESTING
bool request(WiFiClientSecure& client, HTTPClient& http, const char* command,
             char* response, size_t responseCapacity) {
    char url[192];
    const int length = snprintf(url, sizeof(url),
                                "https://%s/httpapi.asp?command=%s",
                                DECCA_WIIM_HOST, command);
    if (length <= 0 || static_cast<size_t>(length) >= sizeof(url)) return false;

    if (!http.begin(client, url)) return false;
    const int statusCode = http.GET();
    if (statusCode != HTTP_CODE_OK) {
        http.end();
        return false;
    }

    if (response != nullptr && responseCapacity > 0U) {
        const String payload = http.getString();
        const size_t bytes = min(payload.length(), responseCapacity - 1U);
        std::memcpy(response, payload.c_str(), bytes);
        response[bytes] = '\0';
    }
    http.end();
    return true;
}

void publishWorkerSnapshot() {
    portENTER_CRITICAL(&g_mux);
    g_sharedSnapshot = g_workerSnapshot;
    portEXIT_CRITICAL(&g_mux);
}

void worker(void*) {
    uint32_t lastPlayerPollMs = 0;
    uint32_t lastMetadataPollMs = 0;
    uint32_t lastFailureMs = 0;
    uint8_t consecutiveFailures = 0;
    char response[3072];
    WiFiClientSecure client;
    client.setInsecure();
    client.setTimeout(kRequestTimeoutMs);
    HTTPClient http;
    http.setConnectTimeout(kRequestTimeoutMs);
    http.setTimeout(kRequestTimeoutMs);
    http.setReuse(true);

    for (;;) {
        if (WiFi.status() != WL_CONNECTED) {
            g_workerSnapshot.status = Status::WaitingForNetwork;
            publishWorkerSnapshot();
            vTaskDelay(pdMS_TO_TICKS(kWorkerDelayMs));
            continue;
        }

        const uint32_t now = millis();
        if (consecutiveFailures > 0U &&
            (now - lastFailureMs) < kRetryIntervalMs) {
            vTaskDelay(pdMS_TO_TICKS(kWorkerDelayMs));
            continue;
        }
        g_workerSnapshot.status = Status::Connecting;

        settings::Source requestedSource;
        uint8_t requestedVolume;
        bool sourceDirty;
        bool volumeDirty;
        bool requestedPowerOn;
        bool powerDirty;
        portENTER_CRITICAL(&g_mux);
        requestedSource = g_requestedSource;
        requestedVolume = g_requestedVolume;
        sourceDirty = g_sourceDirty;
        volumeDirty = g_volumeDirty;
        requestedPowerOn = g_requestedPowerOn;
        powerDirty = g_powerDirty;
        portEXIT_CRITICAL(&g_mux);

        bool success = true;
        if (powerDirty && !requestedPowerOn) {
            success = request(client, http, "setPlayerCmd:stop", nullptr, 0);
            if (success) {
                portENTER_CRITICAL(&g_mux);
                if (!g_requestedPowerOn) g_powerDirty = false;
                portEXIT_CRITICAL(&g_mux);
            }
        } else if (powerDirty && requestedPowerOn) {
            portENTER_CRITICAL(&g_mux);
            if (g_requestedPowerOn) {
                g_powerDirty = false;
                g_sourceDirty = true;
                g_volumeDirty = true;
            }
            portEXIT_CRITICAL(&g_mux);
        } else if (!requestedPowerOn) {
            g_workerSnapshot.playback = Playback::Stopped;
            g_workerSnapshot.metadataValid = false;
            g_workerSnapshot.title[0] = '\0';
            g_workerSnapshot.artist[0] = '\0';
        } else if (sourceDirty) {
            success = request(client, http, commandForSource(requestedSource),
                              nullptr, 0);
            if (success) {
                portENTER_CRITICAL(&g_mux);
                if (requestedSource == g_requestedSource) g_sourceDirty = false;
                portEXIT_CRITICAL(&g_mux);
            }
        } else if (volumeDirty) {
            char command[32];
            snprintf(command, sizeof(command), "setPlayerCmd:vol:%u",
                     static_cast<unsigned>(requestedVolume));
            success = request(client, http, command, nullptr, 0);
            if (success) {
                portENTER_CRITICAL(&g_mux);
                if (requestedVolume == g_requestedVolume) g_volumeDirty = false;
                portEXIT_CRITICAL(&g_mux);
            }
        } else if ((now - lastPlayerPollMs) >= kPlayerPollIntervalMs) {
            response[0] = '\0';
            success = request(client, http, kPlayerStatusCommand, response,
                              sizeof(response)) &&
                      parsePlayer(response, g_workerSnapshot);
            if (success) lastPlayerPollMs = now;
        } else if ((g_workerSnapshot.playback == Playback::Playing ||
                    g_workerSnapshot.playback == Playback::Paused) &&
                   (now - lastMetadataPollMs) >= kMetadataPollIntervalMs) {
            response[0] = '\0';
            success = request(client, http, kMetadataCommand, response,
                              sizeof(response));
            if (success && hasText(response)) {
                success = parseMeta(response, g_workerSnapshot);
            }
            if (success) lastMetadataPollMs = now;
        }

        if (success) {
            consecutiveFailures = 0;
            g_workerSnapshot.status = Status::Ready;
        } else {
            if (consecutiveFailures < kFailureThreshold) {
                ++consecutiveFailures;
            }
            g_workerSnapshot.status =
                consecutiveFailures >= kFailureThreshold
                    ? Status::Error
                    : Status::Connecting;
            lastFailureMs = now;
            portENTER_CRITICAL(&g_mux);
            g_sourceDirty = true;
            g_volumeDirty = true;
            // ON recovery is source/volume reassertion; only a failed OFF stop
            // command needs the power request itself retried.
            g_powerDirty = !g_requestedPowerOn;
            portEXIT_CRITICAL(&g_mux);
        }
        publishWorkerSnapshot();
        vTaskDelay(pdMS_TO_TICKS(kWorkerDelayMs));
    }
}
#endif

}  // namespace

void init() {
    g_publicSnapshot = Snapshot{};
    g_sharedSnapshot = Snapshot{};
    g_workerSnapshot = Snapshot{};
    if (!configured()) {
        Serial.println("[WIIM] disabled: set DECCA_WIIM_HOST in secrets.h");
        return;
    }
    g_publicSnapshot.status = Status::WaitingForNetwork;
    g_sharedSnapshot.status = Status::WaitingForNetwork;
    g_workerSnapshot.status = Status::WaitingForNetwork;
#ifndef PIO_UNIT_TESTING
    xTaskCreatePinnedToCore(worker, "wiim", kWorkerStackBytes, nullptr, 1,
                            &g_task, kWorkerCore);
#endif
}

void update() {
    portENTER_CRITICAL(&g_mux);
    const Snapshot snapshotCopy = g_sharedSnapshot;
    portEXIT_CRITICAL(&g_mux);
    g_publicSnapshot = snapshotCopy;
}

void requestSource(settings::Source source) {
    portENTER_CRITICAL(&g_mux);
    if (g_requestedSource != source) {
        g_requestedSource = source;
        g_sourceDirty = true;
    }
    portEXIT_CRITICAL(&g_mux);
}

void requestVolume(uint8_t volume) {
    volume = constrain(volume, 0, 100);
    portENTER_CRITICAL(&g_mux);
    if (g_requestedVolume != volume) {
        g_requestedVolume = volume;
        g_volumeDirty = true;
    }
    portEXIT_CRITICAL(&g_mux);
}

void requestPower(bool on) {
    portENTER_CRITICAL(&g_mux);
    if (g_requestedPowerOn != on) {
        g_requestedPowerOn = on;
        g_powerDirty = true;
    }
    portEXIT_CRITICAL(&g_mux);
}

bool configured() {
    return hasText(DECCA_WIIM_HOST);
}

const Snapshot& snapshot() {
    return g_publicSnapshot;
}

#ifdef PIO_UNIT_TESTING
namespace testing {
void reset() {
    g_publicSnapshot = Snapshot{};
    g_sharedSnapshot = Snapshot{};
    g_workerSnapshot = Snapshot{};
    g_requestedSource = settings::Source::DigitalStreamer;
    g_requestedVolume = 0;
    g_sourceDirty = true;
    g_volumeDirty = true;
    g_requestedPowerOn = false;
    g_powerDirty = true;
}
bool parsePlayerStatus(const char* json, Snapshot& output) {
    return parsePlayer(json, output);
}
bool parseMetadata(const char* json, Snapshot& output) {
    return parseMeta(json, output);
}
const char* sourceCommand(settings::Source source) {
    return commandForSource(source);
}
}  // namespace testing
#endif

}  // namespace decca::wiim

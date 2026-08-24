/**
 * @file    lighting.cpp
 * @brief   Implementation of the illumination module (see lighting.h).
 *
 */

#include "lighting.h"

#include <Arduino.h>

#include "hardware.h"
#include "settings.h"

namespace decca::lighting {
namespace {

uint8_t g_brightness = 0;
uint8_t g_targetBrightness = 0;
uint32_t g_lastStepMs = 0;

#ifdef PIO_UNIT_TESTING
testing::TimeProvider g_timeProvider = nullptr;
testing::DutyWriter g_dutyWriter = nullptr;
#endif

bool isDial(Zone zone) {
    return zone == Zone::Dial;
}

uint32_t nowMs() {
#ifdef PIO_UNIT_TESTING
    if (g_timeProvider != nullptr) {
        return g_timeProvider();
    }
#endif
    return millis();
}

void writeDuty(uint8_t duty) {
#ifdef PIO_UNIT_TESTING
    if (g_dutyWriter != nullptr) {
        g_dutyWriter(hardware::kDialLightingPwmChannel, duty);
        return;
    }
#endif
    ledcWrite(hardware::kDialLightingPwmChannel, duty);
}

}  // namespace

void init() {
    // hardware::init() configures LEDC. Reassert safe-off before fading to the
    // persisted idle level so reset can never flash the dial at full power.
    g_brightness = 0;
    g_targetBrightness = settings::get().dial;
    g_lastStepMs = nowMs();
    writeDuty(g_brightness);
}

void update() {
    if (g_brightness == g_targetBrightness) {
        return;
    }

    const uint32_t now = nowMs();
    const uint32_t elapsed = now - g_lastStepMs;
    if (elapsed < kFadeStepIntervalMs) {
        return;
    }

    const uint32_t availableSteps = elapsed / kFadeStepIntervalMs;
    const uint8_t distance =
        g_brightness < g_targetBrightness
            ? static_cast<uint8_t>(g_targetBrightness - g_brightness)
            : static_cast<uint8_t>(g_brightness - g_targetBrightness);
    const uint8_t steps =
        availableSteps < distance ? static_cast<uint8_t>(availableSteps)
                                  : distance;

    if (g_brightness < g_targetBrightness) {
        g_brightness = static_cast<uint8_t>(g_brightness + steps);
    } else {
        g_brightness = static_cast<uint8_t>(g_brightness - steps);
    }

    g_lastStepMs += static_cast<uint32_t>(steps) * kFadeStepIntervalMs;
    writeDuty(g_brightness);
}

void setBrightness(Zone zone, uint8_t brightness) {
    if (!isDial(zone) || brightness == g_targetBrightness) {
        return;
    }
    g_targetBrightness = brightness;
    // Idle time must not become accumulated fade credit that makes the next
    // transition jump immediately to its target.
    g_lastStepMs = nowMs();
}

uint8_t brightness(Zone zone) {
    return isDial(zone) ? g_brightness : 0;
}

uint8_t targetBrightness(Zone zone) {
    return isDial(zone) ? g_targetBrightness : 0;
}

#ifdef PIO_UNIT_TESTING
namespace testing {

void setTimeProvider(TimeProvider provider) {
    g_timeProvider = provider;
}

void setDutyWriter(DutyWriter writer) {
    g_dutyWriter = writer;
}

void resetHooks() {
    g_timeProvider = nullptr;
    g_dutyWriter = nullptr;
}

}  // namespace testing
#endif

}  // namespace decca::lighting

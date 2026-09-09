/**
 * @file    lighting.cpp
 * @brief   Implementation of the illumination module (see lighting.h).
 *
 */

#include "lighting.h"

#include <Arduino.h>

#include "hardware.h"
namespace decca::lighting {
namespace {

uint8_t g_brightness = 0;

#ifdef PIO_UNIT_TESTING
testing::DutyWriter g_dutyWriter = nullptr;
#endif

bool isDial(Zone zone) {
    return zone == Zone::Dial;
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
    // hardware::init() configures LEDC. Reassert safe-off so reset can never
    // flash the dial at full power.
    g_brightness = 0;
    writeDuty(g_brightness);
}

void setBrightness(Zone zone, uint8_t brightness) {
    if (!isDial(zone) || brightness == g_brightness) {
        return;
    }
    g_brightness = brightness;
    writeDuty(g_brightness);
}

uint8_t brightness(Zone zone) {
    return isDial(zone) ? g_brightness : 0;
}

#ifdef PIO_UNIT_TESTING
namespace testing {

void setDutyWriter(DutyWriter writer) {
    g_dutyWriter = writer;
}

void resetHooks() {
    g_dutyWriter = nullptr;
}

}  // namespace testing
#endif

}  // namespace decca::lighting

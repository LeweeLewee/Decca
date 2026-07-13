/**
 * @file    lighting.h
 * @brief   Dial and cabinet illumination (PWM-driven).
 *
 * lighting replaces the original lamps with PWM-controlled LEDs. It handles
 * brightness, standby dimming, and any warm-up / fade effects that keep the
 * lighting feeling period-appropriate rather than abruptly digital.
 *
 * Responsibility:  drive illumination outputs; own brightness and effects.
 * Depends on:      hardware (pin map), settings (brightness/standby prefs).
 * Used by:         main; does not read inputs or draw to the display.
 */

#pragma once

#include <cstdint>

namespace decca::lighting {

/**
 * @brief Illumination zones.
 *
 * Placeholder set — expand to match the restored lighting layout.
 */
enum class Zone {
    Dial,
    Cabinet,
};

/**
 * @brief Configure PWM channels and set a safe default state.
 * @pre   hardware::init() has run.
 */
void init();

/**
 * @brief Advance any active fades/effects. Call once per main loop.
 *        Non-blocking.
 */
void update();

/**
 * @brief Set target brightness for a zone.
 * @param zone        Which illumination zone.
 * @param brightness  0 (off) – 255 (full).
 */
void setBrightness(Zone zone, uint8_t brightness);

}  // namespace decca::lighting

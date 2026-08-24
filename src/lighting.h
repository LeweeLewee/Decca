/**
 * @file    lighting.h
 * @brief   Dial illumination (PWM-driven).
 *
 * lighting replaces the original dial lamps with PWM-controlled LEDs. It
 * handles brightness, standby dimming, and fade effects that keep the lighting
 * feeling period-appropriate rather than abruptly digital.
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
 */
enum class Zone {
    Dial,
};

/** Interval between one-count PWM fade steps. */
constexpr uint32_t kFadeStepIntervalMs = 10;

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

/**
 * @brief Read the brightness currently applied to a zone.
 * @return Applied PWM duty in the range 0–255, or 0 for an invalid zone.
 */
uint8_t brightness(Zone zone);

/**
 * @brief Read the active fade target for a zone.
 * @return Target PWM duty in the range 0–255, or 0 for an invalid zone.
 */
uint8_t targetBrightness(Zone zone);

#ifdef PIO_UNIT_TESTING
namespace testing {

using TimeProvider = uint32_t (*)();
using DutyWriter = void (*)(uint8_t channel, uint32_t duty);

/** Replace millis() with a deterministic provider for on-target tests. */
void setTimeProvider(TimeProvider provider);

/** Replace LEDC writes with a deterministic observer for on-target tests. */
void setDutyWriter(DutyWriter writer);

/** Restore the real clock and LEDC output after a deterministic test. */
void resetHooks();

}  // namespace testing
#endif

}  // namespace decca::lighting

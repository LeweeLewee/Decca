/**
 * @file    lighting.h
 * @brief   Dial illumination (PWM-driven).
 *
 * lighting replaces the original dial lamps with PWM-controlled LEDs. It
 * applies brightness changes immediately for every operating transition.
 *
 * Responsibility:  drive illumination outputs; own applied brightness.
 * Depends on:      hardware (pin map).
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

/**
 * @brief Configure PWM channels and set a safe default state.
 * @pre   hardware::init() has run.
 */
void init();

/**
 * @brief Apply brightness immediately for a zone.
 * @param zone        Which illumination zone.
 * @param brightness  0 (off) – 255 (full).
 */
void setBrightness(Zone zone, uint8_t brightness);

/**
 * @brief Read the brightness currently applied to a zone.
 * @return Applied PWM duty in the range 0–255, or 0 for an invalid zone.
 */
uint8_t brightness(Zone zone);

#ifdef PIO_UNIT_TESTING
namespace testing {

using DutyWriter = void (*)(uint8_t channel, uint32_t duty);

/** Replace LEDC writes with a deterministic observer for on-target tests. */
void setDutyWriter(DutyWriter writer);

/** Restore the real LEDC output after a deterministic test. */
void resetHooks();

}  // namespace testing
#endif

}  // namespace decca::lighting

/**
 * @file    hardware.h
 * @brief   Board-level abstraction: pin map and hardware initialisation.
 *
 * hardware is the single source of truth for physical pin assignments and any
 * board-wide setup. Other modules reference pins through the symbols defined
 * here rather than hard-coding numbers, so that a wiring change touches one
 * file only.
 *
 * Responsibility:  own the pin map and board init. Own nothing device-specific.
 * Depends on:      nothing (lowest layer).
 * Used by:         every other module.
 */

#pragma once

#include <cstdint>

namespace decca::hardware {

// ── Pin assignments ─────────────────────────────────────────────────────────
// These assignments match the proposed map in docs/Wiring.md. They have not
// been bench-verified and must remain labelled proposed until physical testing.
constexpr uint8_t kPotVolume = 32;       // ADC1 (proposed)
constexpr uint8_t kPotBass = 33;         // ADC1 (proposed)
constexpr uint8_t kPotTreble = 34;       // ADC1, input-only (proposed)
constexpr uint8_t kPotBalance = 35;      // ADC1, input-only (proposed)
constexpr uint8_t kSwitchOnOff = 19;      // Digital input, internal pull-up (proposed)
constexpr uint8_t kDisplaySda = 21;       // I2C SDA (proposed)
constexpr uint8_t kDisplayScl = 22;       // I2C SCL (proposed)
constexpr uint8_t kDialLightingPwm = 25;  // LEDC PWM output (proposed)

/**
 * @brief Configure pin modes and board-level peripherals.
 *
 * Call once from setup(), before any other module init.
 */
void init();

}  // namespace decca::hardware

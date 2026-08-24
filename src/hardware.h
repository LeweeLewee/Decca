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
// These assignments match docs/Wiring.md. Pot inputs GPIO32–35 and source
// inputs GPIO16, GPIO17 and GPIO23 were bench-verified on 2026-08-24. GPIO18
// and all other assigned pins remain proposed.
constexpr uint8_t kPotVolume = 32;       // ADC1 (bench-verified)
constexpr uint8_t kPotBass = 33;         // ADC1 (bench-verified)
constexpr uint8_t kPotTreble = 34;       // ADC1, input-only (bench-verified)
constexpr uint8_t kPotBalance = 35;      // ADC1, input-only (bench-verified)
constexpr uint8_t kSwitchOnOff = 19;      // Digital input, internal pull-up (proposed)
constexpr uint8_t kButtonVhf = 16;         // Digital input, internal pull-up (bench-verified)
constexpr uint8_t kButtonMw = 17;          // Digital input, internal pull-up (bench-verified)
constexpr uint8_t kButtonLw = 18;          // Digital input, internal pull-up (proposed)
constexpr uint8_t kButtonGram = 23;        // Digital input, internal pull-up (bench-verified)
constexpr uint8_t kDisplaySda = 21;       // I2C SDA (proposed)
constexpr uint8_t kDisplayScl = 22;       // I2C SCL (proposed)
constexpr uint8_t kDialLightingPwm = 25;  // LEDC PWM output (proposed)

// ── Board-level peripheral configuration ────────────────────────────────────
constexpr uint8_t kAdcResolutionBits = 12;
constexpr uint8_t kDialLightingPwmChannel = 0;
constexpr uint32_t kDialLightingPwmFrequencyHz = 5000;
constexpr uint8_t kDialLightingPwmResolutionBits = 8;

/**
 * @brief Configure pin modes and board-level peripherals.
 *
 * Configures all currently assigned Phase 1 pins, ADC1 and the dial-lighting
 * PWM channel. Call once from setup(), before any other module init.
 */
void init();

}  // namespace decca::hardware

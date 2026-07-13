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
// Placeholder values. Confirm against docs/Wiring.md and hardware/Wiring/
// before wiring any hardware. GPIO numbers below are examples only.
//
// constexpr uint8_t kButtonSource   = 0;
// constexpr uint8_t kButtonPower     = 0;
// constexpr uint8_t kPotVolume       = 0;   // ADC-capable pin
// constexpr uint8_t kPotTone         = 0;   // ADC-capable pin
// constexpr uint8_t kLedDial         = 0;   // PWM-capable pin
// constexpr uint8_t kLedCabinet      = 0;   // PWM-capable pin
// constexpr uint8_t kDisplaySda      = 0;
// constexpr uint8_t kDisplayScl      = 0;

/**
 * @brief Configure pin modes and board-level peripherals.
 *
 * Call once from setup(), before any other module init.
 */
void init();

}  // namespace decca::hardware

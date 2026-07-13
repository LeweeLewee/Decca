/**
 * @file    pots.h
 * @brief   Potentiometer input: filtered analogue reads (volume, tone).
 *
 * pots reads the front-panel potentiometers via the ESP32 ADC and applies
 * smoothing/hysteresis so that a settled knob produces a stable value and a
 * moving knob produces smooth changes without ADC jitter.
 *
 * Responsibility:  read and filter analogue controls; expose normalised values.
 * Depends on:      hardware (pin map).
 * Used by:         main (reads values); does not call other modules.
 */

#pragma once

#include <cstdint>

namespace decca::pots {

/**
 * @brief Logical potentiometers on the front panel.
 *
 * Placeholder set — expand to match the restored control layout.
 */
enum class Pot {
    Volume,
    Tone,
};

/**
 * @brief Configure ADC channels and reset filter state.
 * @pre   hardware::init() has run.
 */
void init();

/**
 * @brief Sample and filter all pots. Call once per main loop. Non-blocking.
 */
void update();

/**
 * @brief Read the latest filtered position of a pot.
 * @param pot  Which control to read.
 * @return Normalised position in the range 0–1000 (placeholder scale).
 */
uint16_t value(Pot pot);

}  // namespace decca::pots

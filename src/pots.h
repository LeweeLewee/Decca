/**
 * @file    pots.h
 * @brief   Potentiometer input: filtered ADC1 position reads.
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
 */
enum class Pot {
    Volume,
    Bass,
    Treble,
    Balance,
};

constexpr uint16_t kNormalisedMin = 0;
constexpr uint16_t kNormalisedMax = 1000;
constexpr uint16_t kAdcRawMax = 4095;
constexpr uint32_t kSampleIntervalMs = 10;

/**
 * @brief Per-control ADC calibration and display-stability configuration.
 *
 * rawMin/rawMax are the measured electrical endpoints. deadband is expressed
 * on the normalised 0–1000 scale. Set inverted when clockwise travel produces
 * decreasing raw ADC values.
 */
struct Calibration {
    uint16_t rawMin = 0;
    uint16_t rawMax = kAdcRawMax;
    uint16_t deadband = 2;
    bool inverted = false;
};

/**
 * @brief Reset sampling and filter state for all controls.
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
 * @return Normalised position in the range 0–1000.
 */
uint16_t value(Pot pot);

/**
 * @brief Read the latest smoothed ADC value before normalisation.
 * @param pot  Which control to read.
 * @return Smoothed 12-bit ADC reading in the range 0–4095.
 */
uint16_t rawValue(Pot pot);

/**
 * @brief Apply calibration to one control and reset its filter state.
 * @return true when the calibration is valid and has been accepted.
 */
bool setCalibration(Pot pot, const Calibration& calibration);

/**
 * @brief Return the active calibration for one control.
 */
Calibration calibration(Pot pot);

#ifdef PIO_UNIT_TESTING
namespace testing {

using RawReader = uint16_t (*)(uint8_t pin);

/**
 * @brief Replace ADC reads with a deterministic provider for on-target tests.
 */
void setRawReader(RawReader reader);

/**
 * @brief Restore real ESP32 ADC reads after a deterministic test.
 */
void resetRawReader();

}  // namespace testing
#endif

}  // namespace decca::pots

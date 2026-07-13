/**
 * @file    pots.cpp
 * @brief   Implementation of potentiometer input (see pots.h).
 *
 * @note    No firmware logic implemented yet — documented skeleton only.
 */

#include "pots.h"

#include <Arduino.h>

#include "hardware.h"

namespace decca::pots {

void init() {
    // TODO(phase1): reset filter state for each ADC channel.
}

void update() {
    // TODO(phase1): sample ADC, apply smoothing/hysteresis.
}

uint16_t value(Pot pot) {
    // TODO(phase1): return the latest filtered value for `pot`.
    (void)pot;
    return 0;
}

}  // namespace decca::pots

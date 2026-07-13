/**
 * @file    hardware.cpp
 * @brief   Implementation of the board-level abstraction (see hardware.h).
 *
 * @note    No firmware logic implemented yet — documented skeleton only.
 */

#include "hardware.h"

#include <Arduino.h>

namespace decca::hardware {

void init() {
    // TODO(phase1): set pinMode() for all inputs and outputs.
    // TODO(phase1): configure ADC attenuation/resolution for pot pins.
    // TODO(phase1): configure LEDC (PWM) channels for lighting pins.
}

}  // namespace decca::hardware

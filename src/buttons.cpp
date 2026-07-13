/**
 * @file    buttons.cpp
 * @brief   Implementation of front-panel button input (see buttons.h).
 *
 * @note    No firmware logic implemented yet — documented skeleton only.
 */

#include "buttons.h"

#include <Arduino.h>

#include "hardware.h"

namespace decca::buttons {

void init() {
    // TODO(phase1): initialise debounce state for each button pin.
}

void update() {
    // TODO(phase1): sample pins, apply debounce, enqueue events.
}

Button nextEvent() {
    // TODO(phase1): pop and return the next queued event.
    return Button::None;
}

}  // namespace decca::buttons

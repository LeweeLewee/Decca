/**
 * @file    display.cpp
 * @brief   Implementation of the OLED display module (see display.h).
 *
 * @note    No firmware logic implemented yet — documented skeleton only.
 */

#include "display.h"

#include <Arduino.h>

#include "hardware.h"
#include "settings.h"

namespace decca::display {

void init() {
    // TODO(phase1): bring up the OLED panel and clear the framebuffer.
}

void update() {
    // TODO(phase1): redraw only when the state to be shown has changed.
}

void showStatus(const char* message) {
    // TODO(phase1): render a transient status line.
    (void)message;
}

}  // namespace decca::display

/**
 * @file    lighting.cpp
 * @brief   Implementation of the illumination module (see lighting.h).
 *
 * @note    No firmware logic implemented yet — documented skeleton only.
 */

#include "lighting.h"

#include <Arduino.h>

#include "hardware.h"
#include "settings.h"

namespace decca::lighting {

void init() {
    // TODO(phase1): configure PWM channels; apply default brightness.
}

void update() {
    // TODO(phase1): step active fades toward their targets.
}

void setBrightness(Zone zone, uint8_t brightness) {
    // TODO(phase1): set the fade target for `zone`.
    (void)zone;
    (void)brightness;
}

}  // namespace decca::lighting

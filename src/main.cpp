/**
 * @file    main.cpp
 * @brief   Application entry point and top-level scheduler for decca.
 *
 * main.cpp owns nothing except orchestration. It initialises each module once,
 * then drives them from the main loop. All device behaviour lives inside the
 * modules (buttons, pots, display, lighting, settings); this file only wires
 * them together and defines the update order.
 *
 * Modules must not call into each other directly. Cross-module data flows
 * through `settings` and through values returned by each module's interface.
 *
 * @note  No firmware logic is implemented yet — this is a documented skeleton.
 *        See docs/Firmware Architecture.md for the intended design.
 */

#include <Arduino.h>

// During `pio test`, the module sources in src/ are compiled together with the
// test runner (test_build_src = yes). Each test provides its own setup()/loop(),
// so exclude this firmware entry point from test builds. PlatformIO defines
// PIO_UNIT_TESTING for test builds.
#ifndef PIO_UNIT_TESTING

#include "hardware.h"
#include "settings.h"
#include "buttons.h"
#include "pots.h"
#include "display.h"
#include "lighting.h"

/**
 * @brief One-time initialisation, run at power-on / reset.
 *
 * Initialisation order matters:
 *   1. hardware  — establish pin modes and board-level state first.
 *   2. settings  — load persisted configuration before modules read it.
 *   3. remaining modules — inputs, then outputs.
 */
void setup() {
    // TODO(phase1): decca::hardware::init();
    // TODO(phase1): decca::settings::init();
    // TODO(phase1): decca::buttons::init();
    // TODO(phase1): decca::pots::init();
    // TODO(phase1): decca::display::init();
    // TODO(phase1): decca::lighting::init();
}

/**
 * @brief Cooperative main loop.
 *
 * Each module exposes a non-blocking update() that is called every iteration.
 * Inputs are polled first so that outputs react within the same cycle.
 */
void loop() {
    // TODO(phase1): decca::buttons::update();
    // TODO(phase1): decca::pots::update();
    // TODO(phase1): decca::display::update();
    // TODO(phase1): decca::lighting::update();
}

#endif  // PIO_UNIT_TESTING

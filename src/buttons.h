/**
 * @file    buttons.h
 * @brief   Front-panel button input: debounced, event-based reads.
 *
 * buttons reads the retained on/off switch and four working source buttons,
 * turning raw, noisy GPIO transitions into clean, debounced events that the
 * rest of the firmware can consume without worrying about contact bounce.
 *
 * Responsibility:  read and debounce buttons; expose stable state and presses.
 * Depends on:      hardware (pin map).
 * Used by:         main (dispatches events); does not call other modules.
 */

#pragma once

#include <cstdint>

namespace decca::buttons {

/**
 * @brief Logical buttons on the front panel.
 */
enum class Button {
    None,
    OnOff,
    Vhf,
    Mw,
    Lw,
    Gram,
};

/** Maximum raw-state settling time before a transition is accepted. */
constexpr uint32_t kDebounceMs = 25;

/**
 * @brief Configure button GPIOs and reset debounce state.
 * @pre   hardware::init() has run.
 */
void init();

/**
 * @brief Poll and debounce all buttons. Call once per main loop.
 *        Non-blocking.
 */
void update();

/**
 * @brief Fetch the next debounced button event, if any.
 * @return The pressed Button, or Button::None if the queue is empty.
 */
Button nextEvent();

/**
 * @brief Read the latest debounced state of a front-panel control.
 * @param button  Control to inspect; Button::None always returns false.
 * @return true while the active-low contact is closed.
 */
bool isPressed(Button button);

#ifdef PIO_UNIT_TESTING
namespace testing {

using RawReader = int (*)(uint8_t pin);

/** Replace digital GPIO reads with a deterministic provider for tests. */
void setRawReader(RawReader reader);

/** Restore real ESP32 digital reads after a deterministic test. */
void resetRawReader();

}  // namespace testing
#endif

}  // namespace decca::buttons

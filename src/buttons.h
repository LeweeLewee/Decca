/**
 * @file    buttons.h
 * @brief   Front-panel button input: debounced, event-based reads.
 *
 * buttons reads the retained on/off switch and four working source buttons,
 * turning raw, noisy GPIO transitions into clean, debounced events that the
 * rest of the firmware can consume without worrying about contact bounce.
 *
 * Responsibility:  read and debounce buttons; expose press/hold events.
 * Depends on:      hardware (pin map).
 * Used by:         main (dispatches events); does not call other modules.
 */

#pragma once

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

}  // namespace decca::buttons

/**
 * @file    display.h
 * @brief   OLED display mounted behind the dial glass.
 *
 * display owns the small OLED panel and everything drawn to it: the idle/now-
 * playing screen, volume/source overlays, and (Phase 2+) metadata and menus.
 * It renders state it is given; it does not decide behaviour or read inputs.
 *
 * Responsibility:  render to the OLED; own screen layout and refresh timing.
 * Depends on:      hardware (pin map), settings (what to show).
 * Used by:         main (pushes state to display); does not call inputs.
 */

#pragma once

namespace decca::display {

/**
 * @brief Initialise the OLED panel and clear the screen.
 * @pre   hardware::init() has run.
 */
void init();

/**
 * @brief Redraw as needed. Call once per main loop. Non-blocking;
 *        should only push to the panel when the drawn state changes.
 */
void update();

/**
 * @brief Show a short, transient status line (e.g. "Volume 42").
 * @param message  Null-terminated text to display briefly.
 */
void showStatus(const char* message);

}  // namespace decca::display

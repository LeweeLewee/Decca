/**
 * @file    power.h
 * @brief   Logical Decca system-power state.
 *
 * The retained on/off switch is debounced by buttons. main supplies that stable
 * request here, then coordinates the resulting state into display, lighting and
 * future WiiM/ZA3 outputs. This module owns no GPIO and remains non-blocking.
 */
#pragma once

#include <cstdint>

namespace decca::power {

enum class State : uint8_t {
    Standby,
    On,
};

/** Initialise from the already-debounced retained switch state. */
void init(bool requestedOn);

/**
 * Apply the latest stable switch request.
 * @return true only when the logical power state changes.
 */
bool update(bool requestedOn);

/** Return the current logical system-power state. */
State state();

/** Convenience query for output coordination in main. */
bool isOn();

}  // namespace decca::power

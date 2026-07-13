/**
 * @file    settings.cpp
 * @brief   Implementation of persisted configuration/state (see settings.h).
 *
 * @note    No firmware logic implemented yet — documented skeleton only.
 */

#include "settings.h"

#include <Arduino.h>

namespace decca::settings {

namespace {
State g_state;  // in-RAM snapshot; persisted lazily via save().
}

void init() {
    // TODO(phase1): open NVS namespace; load persisted values or defaults.
}

const State& get() {
    return g_state;
}

void set(const State& state) {
    // TODO(phase1): copy in and mark dirty.
    g_state = state;
}

void save() {
    // TODO(phase1): if dirty, write g_state to NVS and clear the dirty flag.
}

}  // namespace decca::settings

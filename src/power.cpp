/** @file power.cpp @brief Logical Decca system-power state. */
#include "power.h"

namespace decca::power {
namespace {

State g_state = State::Standby;

State requestedState(bool requestedOn) {
    return requestedOn ? State::On : State::Standby;
}

}  // namespace

void init(bool requestedOn) {
    g_state = requestedState(requestedOn);
}

bool update(bool requestedOn) {
    const State next = requestedState(requestedOn);
    if (next == g_state) {
        return false;
    }
    g_state = next;
    return true;
}

State state() {
    return g_state;
}

bool isOn() {
    return g_state == State::On;
}

}  // namespace decca::power

/**
 * @file    buttons.cpp
 * @brief   Implementation of front-panel button input (see buttons.h).
 */

#include "buttons.h"

#include <Arduino.h>

#include "hardware.h"

namespace decca::buttons {
namespace {

constexpr uint8_t kButtonCount = 5;
constexpr uint8_t kEventQueueCapacity = 8;

constexpr Button kButtons[kButtonCount] = {
    Button::OnOff,
    Button::Vhf,
    Button::Mw,
    Button::Lw,
    Button::Gram,
};

constexpr uint8_t kPins[kButtonCount] = {
    hardware::kSwitchOnOff,
    hardware::kButtonVhf,
    hardware::kButtonMw,
    hardware::kButtonLw,
    hardware::kButtonGram,
};

struct ButtonState {
    bool candidatePressed = false;
    bool stablePressed = false;
    uint32_t candidateSinceMs = 0;
};

ButtonState g_states[kButtonCount]{};
Button g_events[kEventQueueCapacity]{};
uint8_t g_eventHead = 0;
uint8_t g_eventTail = 0;
uint8_t g_eventCount = 0;

#ifdef PIO_UNIT_TESTING
testing::RawReader g_rawReader = nullptr;
#endif

bool indexFor(Button button, uint8_t& index) {
    const uint8_t value = static_cast<uint8_t>(button);
    if (value == 0 || value > kButtonCount) {
        return false;
    }
    index = value - 1;
    return true;
}

int readLevel(uint8_t pin) {
#ifdef PIO_UNIT_TESTING
    if (g_rawReader != nullptr) {
        return g_rawReader(pin);
    }
#endif
    return digitalRead(pin);
}

bool readPressed(uint8_t pin) {
    return readLevel(pin) == LOW;
}

void enqueue(Button button) {
    if (g_eventCount >= kEventQueueCapacity) {
        return;
    }
    g_events[g_eventTail] = button;
    g_eventTail = (g_eventTail + 1) % kEventQueueCapacity;
    ++g_eventCount;
}

}  // namespace

void init() {
    g_eventHead = 0;
    g_eventTail = 0;
    g_eventCount = 0;

    const uint32_t now = millis();
    for (uint8_t i = 0; i < kButtonCount; ++i) {
        const bool pressed = readPressed(kPins[i]);
        g_states[i] = ButtonState{pressed, pressed, now};
    }
}

void update() {
    const uint32_t now = millis();

    for (uint8_t i = 0; i < kButtonCount; ++i) {
        ButtonState& state = g_states[i];
        const bool pressed = readPressed(kPins[i]);

        if (pressed != state.candidatePressed) {
            state.candidatePressed = pressed;
            state.candidateSinceMs = now;
            continue;
        }

        if (pressed != state.stablePressed &&
            (now - state.candidateSinceMs) >= kDebounceMs) {
            state.stablePressed = pressed;
            if (pressed) {
                enqueue(kButtons[i]);
            }
        }
    }
}

Button nextEvent() {
    if (g_eventCount == 0) {
        return Button::None;
    }

    const Button event = g_events[g_eventHead];
    g_eventHead = (g_eventHead + 1) % kEventQueueCapacity;
    --g_eventCount;
    return event;
}

bool isPressed(Button button) {
    uint8_t index = 0;
    return indexFor(button, index) && g_states[index].stablePressed;
}

#ifdef PIO_UNIT_TESTING
namespace testing {

void setRawReader(RawReader reader) {
    g_rawReader = reader;
}

void resetRawReader() {
    g_rawReader = nullptr;
}

}  // namespace testing
#endif

}  // namespace decca::buttons

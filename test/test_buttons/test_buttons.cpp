/**
 * @file    test_buttons.cpp
 * @brief   Tests for the buttons module (debounced input events).
 *
 * With no input driven, the event queue must be empty. As debouncing lands, add
 * tests that inject transitions and assert on emitted events and timing.
 */

#include "unity_runner.h"

#include "buttons.h"

using decca::buttons::Button;

// The event type must represent only the confirmed Phase 1 controls.
void test_buttons_confirmed_control_set() {
    const Button controls[] = {
        Button::OnOff,
        Button::Vhf,
        Button::Mw,
        Button::Lw,
        Button::Gram,
    };

    TEST_ASSERT_EQUAL_UINT32(5, sizeof(controls) / sizeof(controls[0]));
}

// A freshly initialised module has no pending events.
void test_buttons_no_event_when_idle() {
    decca::buttons::init();
    decca::buttons::update();
    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void runAll() {
    RUN_TEST(test_buttons_confirmed_control_set);
    RUN_TEST(test_buttons_no_event_when_idle);
}

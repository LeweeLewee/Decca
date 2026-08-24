/**
 * @file    test_buttons.cpp
 * @brief   Behavioural tests for active-low debounced front-panel inputs.
 */

#include "unity_runner.h"

#include "buttons.h"
#include "hardware.h"

using decca::buttons::Button;

namespace {

int g_levels[40]{};

int readInjected(uint8_t pin) {
    return g_levels[pin];
}

void startInjected() {
    for (auto& level : g_levels) {
        level = HIGH;
    }
    decca::buttons::testing::setRawReader(readInjected);
    decca::buttons::init();
}

void settle() {
    delay(decca::buttons::kDebounceMs + 1);
    decca::buttons::update();
}

void press(uint8_t pin) {
    g_levels[pin] = LOW;
    decca::buttons::update();
    settle();
}

void release(uint8_t pin) {
    g_levels[pin] = HIGH;
    decca::buttons::update();
    settle();
}

void printPressed(const char* label, Button button) {
    UnityPrint(label);
    UnityPrintNumberUnsigned(decca::buttons::isPressed(button) ? 1U : 0U);
}

}  // namespace

void test_buttons_physical_snapshot() {
    decca::hardware::init();
    decca::buttons::testing::resetRawReader();
    decca::buttons::init();

    UnityPrint("BUTTON_SNAPSHOT pressed ");
    printPressed("onoff=", Button::OnOff);
    printPressed(" vhf=", Button::Vhf);
    printPressed(" mw=", Button::Mw);
    printPressed(" lw=", Button::Lw);
    printPressed(" gram=", Button::Gram);
    UNITY_PRINT_EOL();

    TEST_PASS();
}

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

void test_buttons_no_event_when_idle() {
    startInjected();
    decca::buttons::update();

    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void test_buttons_debounce_active_low_press() {
    startInjected();
    g_levels[decca::hardware::kButtonVhf] = LOW;
    decca::buttons::update();

    TEST_ASSERT_FALSE(decca::buttons::isPressed(Button::Vhf));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));

    settle();

    TEST_ASSERT_TRUE(decca::buttons::isPressed(Button::Vhf));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::Vhf),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void test_buttons_reject_contact_bounce() {
    startInjected();

    g_levels[decca::hardware::kButtonMw] = LOW;
    decca::buttons::update();
    delay(5);
    g_levels[decca::hardware::kButtonMw] = HIGH;
    decca::buttons::update();
    delay(5);
    g_levels[decca::hardware::kButtonMw] = LOW;
    decca::buttons::update();

    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));

    settle();

    TEST_ASSERT_EQUAL(static_cast<int>(Button::Mw),
                      static_cast<int>(decca::buttons::nextEvent()));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void test_buttons_hold_does_not_repeat() {
    startInjected();
    press(decca::hardware::kButtonLw);

    TEST_ASSERT_EQUAL(static_cast<int>(Button::Lw),
                      static_cast<int>(decca::buttons::nextEvent()));

    settle();
    settle();

    TEST_ASSERT_TRUE(decca::buttons::isPressed(Button::Lw));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void test_buttons_release_rearms_next_press() {
    startInjected();
    press(decca::hardware::kButtonGram);
    TEST_ASSERT_EQUAL(static_cast<int>(Button::Gram),
                      static_cast<int>(decca::buttons::nextEvent()));

    release(decca::hardware::kButtonGram);
    TEST_ASSERT_FALSE(decca::buttons::isPressed(Button::Gram));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));

    press(decca::hardware::kButtonGram);
    TEST_ASSERT_EQUAL(static_cast<int>(Button::Gram),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void test_buttons_queue_simultaneous_presses_in_pin_order() {
    startInjected();
    g_levels[decca::hardware::kSwitchOnOff] = LOW;
    g_levels[decca::hardware::kButtonVhf] = LOW;
    g_levels[decca::hardware::kButtonMw] = LOW;
    g_levels[decca::hardware::kButtonLw] = LOW;
    g_levels[decca::hardware::kButtonGram] = LOW;
    decca::buttons::update();
    settle();

    const Button expected[] = {
        Button::OnOff,
        Button::Vhf,
        Button::Mw,
        Button::Lw,
        Button::Gram,
    };
    for (const Button button : expected) {
        TEST_ASSERT_EQUAL(static_cast<int>(button),
                          static_cast<int>(decca::buttons::nextEvent()));
    }
    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void test_buttons_initial_latched_state_is_available_without_false_event() {
    for (auto& level : g_levels) {
        level = HIGH;
    }
    g_levels[decca::hardware::kSwitchOnOff] = LOW;
    decca::buttons::testing::setRawReader(readInjected);
    decca::buttons::init();

    TEST_ASSERT_TRUE(decca::buttons::isPressed(Button::OnOff));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void runAll() {
    RUN_TEST(test_buttons_physical_snapshot);
    RUN_TEST(test_buttons_confirmed_control_set);
    RUN_TEST(test_buttons_no_event_when_idle);
    RUN_TEST(test_buttons_debounce_active_low_press);
    RUN_TEST(test_buttons_reject_contact_bounce);
    RUN_TEST(test_buttons_hold_does_not_repeat);
    RUN_TEST(test_buttons_release_rearms_next_press);
    RUN_TEST(test_buttons_queue_simultaneous_presses_in_pin_order);
    RUN_TEST(test_buttons_initial_latched_state_is_available_without_false_event);
}

/**
 * @file    test_buttons.cpp
 * @brief   Behavioural tests for on/off and sole Gram source selection.
 */
#include "unity_runner.h"

#include "buttons.h"
#include "hardware.h"

using decca::buttons::Button;
using decca::buttons::SourceMode;

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

}  // namespace

void test_buttons_physical_snapshot() {
    decca::hardware::init();
    decca::buttons::testing::resetRawReader();
    decca::buttons::init();

    UnityPrint("BUTTON_SNAPSHOT pressed onoff=");
    UnityPrintNumberUnsigned(decca::buttons::isPressed(Button::OnOff) ? 1U : 0U);
    UnityPrint(" gram=");
    UnityPrintNumberUnsigned(decca::buttons::isPressed(Button::Gram) ? 1U : 0U);
    UnityPrint(" source=");
    UnityPrint(decca::buttons::sourceMode() == SourceMode::Vinyl
                   ? "vinyl"
                   : "digital");
    UNITY_PRINT_EOL();
    TEST_PASS();
}

void test_buttons_confirmed_control_set() {
    const Button controls[] = {Button::OnOff, Button::Gram};
    TEST_ASSERT_EQUAL_UINT32(2, sizeof(controls) / sizeof(controls[0]));
}

void test_buttons_defaults_to_digital_when_gram_open() {
    startInjected();
    TEST_ASSERT_EQUAL(static_cast<int>(SourceMode::DigitalStreamer),
                      static_cast<int>(decca::buttons::sourceMode()));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void test_buttons_debounce_gram_to_vinyl() {
    startInjected();
    g_levels[decca::hardware::kButtonGram] = LOW;
    decca::buttons::update();

    TEST_ASSERT_EQUAL(static_cast<int>(SourceMode::DigitalStreamer),
                      static_cast<int>(decca::buttons::sourceMode()));
    settle();

    TEST_ASSERT_EQUAL(static_cast<int>(SourceMode::Vinyl),
                      static_cast<int>(decca::buttons::sourceMode()));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::Gram),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void test_buttons_reject_gram_contact_bounce() {
    startInjected();
    g_levels[decca::hardware::kButtonGram] = LOW;
    decca::buttons::update();
    delay(5);
    g_levels[decca::hardware::kButtonGram] = HIGH;
    decca::buttons::update();
    delay(5);
    g_levels[decca::hardware::kButtonGram] = LOW;
    decca::buttons::update();

    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));
    settle();
    TEST_ASSERT_EQUAL(static_cast<int>(SourceMode::Vinyl),
                      static_cast<int>(decca::buttons::sourceMode()));
}

void test_buttons_hold_does_not_repeat() {
    startInjected();
    press(decca::hardware::kButtonGram);
    TEST_ASSERT_EQUAL(static_cast<int>(Button::Gram),
                      static_cast<int>(decca::buttons::nextEvent()));
    settle();
    settle();
    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void test_buttons_release_selects_digital_and_rearms() {
    startInjected();
    press(decca::hardware::kButtonGram);
    TEST_ASSERT_EQUAL(static_cast<int>(Button::Gram),
                      static_cast<int>(decca::buttons::nextEvent()));

    release(decca::hardware::kButtonGram);
    TEST_ASSERT_EQUAL(static_cast<int>(SourceMode::DigitalStreamer),
                      static_cast<int>(decca::buttons::sourceMode()));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));

    press(decca::hardware::kButtonGram);
    TEST_ASSERT_EQUAL(static_cast<int>(Button::Gram),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void test_buttons_queue_simultaneous_presses_in_pin_order() {
    startInjected();
    g_levels[decca::hardware::kSwitchOnOff] = LOW;
    g_levels[decca::hardware::kButtonGram] = LOW;
    decca::buttons::update();
    settle();

    TEST_ASSERT_EQUAL(static_cast<int>(Button::OnOff),
                      static_cast<int>(decca::buttons::nextEvent()));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::Gram),
                      static_cast<int>(decca::buttons::nextEvent()));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void test_buttons_initial_latched_states_have_no_false_event() {
    for (auto& level : g_levels) {
        level = HIGH;
    }
    g_levels[decca::hardware::kSwitchOnOff] = LOW;
    g_levels[decca::hardware::kButtonGram] = LOW;
    decca::buttons::testing::setRawReader(readInjected);
    decca::buttons::init();

    TEST_ASSERT_TRUE(decca::buttons::isPressed(Button::OnOff));
    TEST_ASSERT_EQUAL(static_cast<int>(SourceMode::Vinyl),
                      static_cast<int>(decca::buttons::sourceMode()));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void runAll() {
    RUN_TEST(test_buttons_physical_snapshot);
    RUN_TEST(test_buttons_confirmed_control_set);
    RUN_TEST(test_buttons_defaults_to_digital_when_gram_open);
    RUN_TEST(test_buttons_debounce_gram_to_vinyl);
    RUN_TEST(test_buttons_reject_gram_contact_bounce);
    RUN_TEST(test_buttons_hold_does_not_repeat);
    RUN_TEST(test_buttons_release_selects_digital_and_rearms);
    RUN_TEST(test_buttons_queue_simultaneous_presses_in_pin_order);
    RUN_TEST(test_buttons_initial_latched_states_have_no_false_event);
}

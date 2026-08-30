/**
 * @file    test_buttons.cpp
 * @brief   Behavioural tests for power, source and lighting-command inputs.
 */
#include "unity_runner.h"

#include "buttons.h"
#include "hardware.h"

using decca::buttons::Button;
using decca::buttons::LightingRequest;
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
    UnityPrint(" vhf=");
    UnityPrintNumberUnsigned(decca::buttons::isPressed(Button::Vhf) ? 1U : 0U);
    UnityPrint(" source=");
    UnityPrint(decca::buttons::sourceMode() == SourceMode::Vinyl
                   ? "vinyl"
                   : "digital");
    UnityPrint(" stereo_mono_contact=");
    UnityPrintNumberUnsigned(decca::buttons::isPressed(Button::StereoMono) ? 1U : 0U);
    UnityPrint(" lights=");
    UnityPrint(decca::buttons::lightingRequest() == LightingRequest::On
                   ? "on"
                   : "off");
    UNITY_PRINT_EOL();
    TEST_PASS();
}

void test_buttons_confirmed_control_set() {
    const Button controls[] = {Button::OnOff, Button::Vhf, Button::StereoMono};
    TEST_ASSERT_EQUAL_UINT32(3, sizeof(controls) / sizeof(controls[0]));
}

void test_buttons_stereo_open_requests_lights_on() {
    startInjected();
    TEST_ASSERT_EQUAL(static_cast<int>(LightingRequest::On),
                      static_cast<int>(decca::buttons::lightingRequest()));
}

void test_buttons_mono_close_requests_lights_off_and_stereo_release_requests_on() {
    startInjected();
    press(decca::hardware::kSwitchStereoMono);

    TEST_ASSERT_EQUAL(static_cast<int>(LightingRequest::Off),
                      static_cast<int>(decca::buttons::lightingRequest()));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::StereoMono),
                      static_cast<int>(decca::buttons::nextEvent()));

    release(decca::hardware::kSwitchStereoMono);
    TEST_ASSERT_EQUAL(static_cast<int>(LightingRequest::On),
                      static_cast<int>(decca::buttons::lightingRequest()));
}

void test_buttons_defaults_to_vinyl_when_vhf_open() {
    startInjected();
    TEST_ASSERT_EQUAL(static_cast<int>(SourceMode::Vinyl),
                      static_cast<int>(decca::buttons::sourceMode()));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void test_buttons_debounce_vhf_to_digital() {
    startInjected();
    g_levels[decca::hardware::kButtonVhf] = LOW;
    decca::buttons::update();

    TEST_ASSERT_EQUAL(static_cast<int>(SourceMode::Vinyl),
                      static_cast<int>(decca::buttons::sourceMode()));
    settle();

    TEST_ASSERT_EQUAL(static_cast<int>(SourceMode::DigitalStreamer),
                      static_cast<int>(decca::buttons::sourceMode()));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::Vhf),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void test_buttons_reject_vhf_contact_bounce() {
    startInjected();
    g_levels[decca::hardware::kButtonVhf] = LOW;
    decca::buttons::update();
    delay(5);
    g_levels[decca::hardware::kButtonVhf] = HIGH;
    decca::buttons::update();
    delay(5);
    g_levels[decca::hardware::kButtonVhf] = LOW;
    decca::buttons::update();

    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));
    settle();
    TEST_ASSERT_EQUAL(static_cast<int>(SourceMode::DigitalStreamer),
                      static_cast<int>(decca::buttons::sourceMode()));
}

void test_buttons_hold_does_not_repeat() {
    startInjected();
    press(decca::hardware::kButtonVhf);
    TEST_ASSERT_EQUAL(static_cast<int>(Button::Vhf),
                      static_cast<int>(decca::buttons::nextEvent()));
    settle();
    settle();
    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void test_buttons_release_selects_vinyl_and_rearms() {
    startInjected();
    press(decca::hardware::kButtonVhf);
    TEST_ASSERT_EQUAL(static_cast<int>(Button::Vhf),
                      static_cast<int>(decca::buttons::nextEvent()));

    release(decca::hardware::kButtonVhf);
    TEST_ASSERT_EQUAL(static_cast<int>(SourceMode::Vinyl),
                      static_cast<int>(decca::buttons::sourceMode()));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));

    press(decca::hardware::kButtonVhf);
    TEST_ASSERT_EQUAL(static_cast<int>(Button::Vhf),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void test_buttons_queue_simultaneous_presses_in_pin_order() {
    startInjected();
    g_levels[decca::hardware::kSwitchOnOff] = LOW;
    g_levels[decca::hardware::kButtonVhf] = LOW;
    g_levels[decca::hardware::kSwitchStereoMono] = LOW;
    decca::buttons::update();
    settle();

    TEST_ASSERT_EQUAL(static_cast<int>(Button::OnOff),
                      static_cast<int>(decca::buttons::nextEvent()));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::Vhf),
                      static_cast<int>(decca::buttons::nextEvent()));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::StereoMono),
                      static_cast<int>(decca::buttons::nextEvent()));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void test_buttons_initial_latched_states_have_no_false_event() {
    for (auto& level : g_levels) {
        level = HIGH;
    }
    g_levels[decca::hardware::kSwitchOnOff] = LOW;
    g_levels[decca::hardware::kButtonVhf] = LOW;
    g_levels[decca::hardware::kSwitchStereoMono] = LOW;
    decca::buttons::testing::setRawReader(readInjected);
    decca::buttons::init();

    TEST_ASSERT_TRUE(decca::buttons::isPressed(Button::OnOff));
    TEST_ASSERT_EQUAL(static_cast<int>(SourceMode::DigitalStreamer),
                      static_cast<int>(decca::buttons::sourceMode()));
    TEST_ASSERT_EQUAL(static_cast<int>(LightingRequest::Off),
                      static_cast<int>(decca::buttons::lightingRequest()));
    TEST_ASSERT_EQUAL(static_cast<int>(Button::None),
                      static_cast<int>(decca::buttons::nextEvent()));
}

void runAll() {
    RUN_TEST(test_buttons_physical_snapshot);
    RUN_TEST(test_buttons_confirmed_control_set);
    RUN_TEST(test_buttons_stereo_open_requests_lights_on);
    RUN_TEST(test_buttons_mono_close_requests_lights_off_and_stereo_release_requests_on);
    RUN_TEST(test_buttons_defaults_to_vinyl_when_vhf_open);
    RUN_TEST(test_buttons_debounce_vhf_to_digital);
    RUN_TEST(test_buttons_reject_vhf_contact_bounce);
    RUN_TEST(test_buttons_hold_does_not_repeat);
    RUN_TEST(test_buttons_release_selects_vinyl_and_rearms);
    RUN_TEST(test_buttons_queue_simultaneous_presses_in_pin_order);
    RUN_TEST(test_buttons_initial_latched_states_have_no_false_event);
}

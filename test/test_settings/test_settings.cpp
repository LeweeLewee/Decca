/**
 * @file    test_settings.cpp
 * @brief   Tests for the settings module (shared state + persistence).
 *
 * The round-trip test is already meaningful against the current stub: set()
 * copies into the in-RAM snapshot and get() returns it. As NVS persistence
 * lands, add tests that survive a reload.
 */

#include "unity_runner.h"

#include "settings.h"

using decca::settings::State;
using decca::settings::Source;

// Fresh state should hold safe defaults.
void test_settings_defaults() {
    decca::settings::init();
    const State& s = decca::settings::get();
    TEST_ASSERT_EQUAL(static_cast<int>(Source::Vhf), static_cast<int>(s.source));
    TEST_ASSERT_EQUAL_UINT8(0, s.volume);
    TEST_ASSERT_EQUAL_UINT8(0, s.dial);
}

// set() then get() must round-trip the values.
void test_settings_set_get_roundtrip() {
    State next;
    next.source = Source::Gram;
    next.volume = 42;
    next.dial = 128;
    decca::settings::set(next);

    const State& s = decca::settings::get();
    TEST_ASSERT_EQUAL(static_cast<int>(Source::Gram), static_cast<int>(s.source));
    TEST_ASSERT_EQUAL_UINT8(42, s.volume);
    TEST_ASSERT_EQUAL_UINT8(128, s.dial);
}

// save() must be callable without faulting (no-op until NVS lands).
void test_settings_save_is_callable() {
    decca::settings::save();
    TEST_PASS();
}

void runAll() {
    RUN_TEST(test_settings_defaults);
    RUN_TEST(test_settings_set_get_roundtrip);
    RUN_TEST(test_settings_save_is_callable);
}

/**
 * @file    test_settings.cpp
 * @brief   Tests for the settings module (shared state + persistence).
 *
 * Tests use the real ESP32 NVS backend under a test-only namespace so they do
 * not alter production settings.
 */

#include "unity_runner.h"

#include "settings.h"

using decca::settings::State;
using decca::settings::Source;

void assertStateEquals(const State& expected, const State& actual) {
    TEST_ASSERT_EQUAL(static_cast<int>(expected.source),
                      static_cast<int>(actual.source));
    TEST_ASSERT_EQUAL_UINT8(expected.volume, actual.volume);
    TEST_ASSERT_EQUAL_UINT8(expected.dial, actual.dial);
}

// A default-constructed snapshot must hold safe first-boot values.
void test_settings_defaults() {
    const State defaults;
    TEST_ASSERT_EQUAL(static_cast<int>(Source::Vhf),
                      static_cast<int>(defaults.source));
    TEST_ASSERT_EQUAL_UINT8(0, defaults.volume);
    TEST_ASSERT_EQUAL_UINT8(0, defaults.dial);
}

// set() then get() must round-trip the values.
void test_settings_set_get_roundtrip() {
    State next;
    next.source = Source::Gram;
    next.volume = 42;
    next.dial = 128;
    decca::settings::set(next);

    assertStateEquals(next, decca::settings::get());
}

// Saved settings must survive module reinitialisation through the NVS backend.
void test_settings_nvs_roundtrip() {
    const State first{Source::Mw, 73, 141};
    const State second{Source::Lw, 184, 62};

    decca::settings::init();
    decca::settings::set(first);
    decca::settings::save();
    decca::settings::init();
    assertStateEquals(first, decca::settings::get());

    decca::settings::set(second);
    decca::settings::save();
    decca::settings::set(first);  // Deliberately leave RAM different from NVS.
    decca::settings::init();
    assertStateEquals(second, decca::settings::get());
}

void runAll() {
    RUN_TEST(test_settings_defaults);
    RUN_TEST(test_settings_set_get_roundtrip);
    RUN_TEST(test_settings_nvs_roundtrip);
}

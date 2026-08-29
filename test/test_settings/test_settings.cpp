/**
 * @file    test_settings.cpp
 * @brief   Settings tests for runtime source and persisted user values.
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

void test_settings_defaults() {
    const State defaults;
    TEST_ASSERT_EQUAL(static_cast<int>(Source::DigitalStreamer),
                      static_cast<int>(defaults.source));
    TEST_ASSERT_EQUAL_UINT8(0, defaults.volume);
    TEST_ASSERT_EQUAL_UINT8(0, defaults.dial);
}

void test_settings_set_get_roundtrip() {
    const State next{Source::Vinyl, 42, 128};
    decca::settings::set(next);
    assertStateEquals(next, decca::settings::get());
}

void test_settings_nvs_roundtrip_does_not_persist_physical_source() {
    const State first{Source::Vinyl, 73, 141};
    const State expectedFirst{Source::DigitalStreamer, 73, 141};
    const State second{Source::Vinyl, 184, 62};
    const State expectedSecond{Source::DigitalStreamer, 184, 62};

    decca::settings::init();
    decca::settings::set(first);
    decca::settings::save();
    decca::settings::init();
    assertStateEquals(expectedFirst, decca::settings::get());

    decca::settings::set(second);
    decca::settings::save();
    decca::settings::set(first);
    decca::settings::init();
    assertStateEquals(expectedSecond, decca::settings::get());
}

void runAll() {
    RUN_TEST(test_settings_defaults);
    RUN_TEST(test_settings_set_get_roundtrip);
    RUN_TEST(test_settings_nvs_roundtrip_does_not_persist_physical_source);
}

/**
 * @file    test_pots.cpp
 * @brief   Behavioural tests for filtered, calibrated analogue input.
 */

#include "unity_runner.h"

#include "hardware.h"
#include "pots.h"

using decca::pots::Pot;

namespace {

uint16_t g_samples[40]{};

uint16_t readInjected(uint8_t pin) {
    return g_samples[pin];
}

void startInjected() {
    for (auto& sample : g_samples) {
        sample = 0;
    }
    decca::pots::init();
    decca::pots::testing::setRawReader(readInjected);
}

void waitForSample() {
    delay(decca::pots::kSampleIntervalMs);
}

}  // namespace

void test_pots_physical_snapshot_is_in_adc_range() {
    decca::hardware::init();
    decca::pots::testing::resetRawReader();
    decca::pots::init();
    decca::pots::update();

    Serial.printf(
        "POT_SNAPSHOT raw volume=%u bass=%u treble=%u balance=%u\n",
        decca::pots::rawValue(Pot::Volume),
        decca::pots::rawValue(Pot::Bass),
        decca::pots::rawValue(Pot::Treble),
        decca::pots::rawValue(Pot::Balance));

    TEST_ASSERT_LESS_OR_EQUAL_UINT16(
        decca::pots::kAdcRawMax, decca::pots::rawValue(Pot::Volume));
    TEST_ASSERT_LESS_OR_EQUAL_UINT16(
        decca::pots::kAdcRawMax, decca::pots::rawValue(Pot::Bass));
    TEST_ASSERT_LESS_OR_EQUAL_UINT16(
        decca::pots::kAdcRawMax, decca::pots::rawValue(Pot::Treble));
    TEST_ASSERT_LESS_OR_EQUAL_UINT16(
        decca::pots::kAdcRawMax, decca::pots::rawValue(Pot::Balance));
}

void test_pots_read_all_four_named_adc_channels() {
    startInjected();
    g_samples[decca::hardware::kPotVolume] = 0;
    g_samples[decca::hardware::kPotBass] = 1024;
    g_samples[decca::hardware::kPotTreble] = 2048;
    g_samples[decca::hardware::kPotBalance] = 4095;

    decca::pots::update();

    TEST_ASSERT_EQUAL_UINT16(0, decca::pots::value(Pot::Volume));
    TEST_ASSERT_UINT16_WITHIN(1, 250, decca::pots::value(Pot::Bass));
    TEST_ASSERT_UINT16_WITHIN(1, 500, decca::pots::value(Pot::Treble));
    TEST_ASSERT_EQUAL_UINT16(1000, decca::pots::value(Pot::Balance));
}

void test_pots_smooth_step_changes() {
    startInjected();
    decca::pots::update();

    g_samples[decca::hardware::kPotVolume] = 4095;
    waitForSample();
    decca::pots::update();

    TEST_ASSERT_UINT16_WITHIN(1, 125, decca::pots::value(Pot::Volume));
    TEST_ASSERT_LESS_THAN_UINT16(4095,
                                 decca::pots::rawValue(Pot::Volume));
}

void test_pots_apply_calibration_and_inversion() {
    startInjected();
    const decca::pots::Calibration inverted{1000, 3000, 0, true};
    TEST_ASSERT_TRUE(decca::pots::setCalibration(Pot::Volume, inverted));

    g_samples[decca::hardware::kPotVolume] = 1000;
    decca::pots::update();

    TEST_ASSERT_EQUAL_UINT16(1000, decca::pots::value(Pot::Volume));
    TEST_ASSERT_EQUAL_UINT16(1000, decca::pots::rawValue(Pot::Volume));
    TEST_ASSERT_TRUE(decca::pots::calibration(Pot::Volume).inverted);
}

void test_pots_hold_changes_below_deadband() {
    startInjected();
    g_samples[decca::hardware::kPotVolume] = 2048;
    decca::pots::update();
    const uint16_t settled = decca::pots::value(Pot::Volume);

    g_samples[decca::hardware::kPotVolume] = 2080;
    waitForSample();
    decca::pots::update();

    TEST_ASSERT_EQUAL_UINT16(settled,
                             decca::pots::value(Pot::Volume));
    TEST_ASSERT_GREATER_THAN_UINT16(2048,
                                    decca::pots::rawValue(Pot::Volume));
}

void test_pots_reject_invalid_calibration() {
    startInjected();
    const decca::pots::Calibration invalid{3000, 1000, 2, false};
    TEST_ASSERT_FALSE(decca::pots::setCalibration(Pot::Volume, invalid));
}

void runAll() {
    RUN_TEST(test_pots_physical_snapshot_is_in_adc_range);
    RUN_TEST(test_pots_read_all_four_named_adc_channels);
    RUN_TEST(test_pots_smooth_step_changes);
    RUN_TEST(test_pots_apply_calibration_and_inversion);
    RUN_TEST(test_pots_hold_changes_below_deadband);
    RUN_TEST(test_pots_reject_invalid_calibration);
}

/**
 * @file    test_hardware.cpp
 * @brief   Interface smoke tests for the hardware module.
 *
 * These confirm the pin-map contract and exercise the real
 * board-initialisation entry point.
 */

#include "unity_runner.h"

#include "hardware.h"

// Named constants and their verification status must match docs/Wiring.md.
void test_hardware_pin_map_contract() {
    TEST_ASSERT_EQUAL_UINT8(32, decca::hardware::kPotVolume);
    TEST_ASSERT_EQUAL_UINT8(33, decca::hardware::kPotBass);
    TEST_ASSERT_EQUAL_UINT8(34, decca::hardware::kPotTreble);
    TEST_ASSERT_EQUAL_UINT8(35, decca::hardware::kPotBalance);
    TEST_ASSERT_EQUAL_UINT8(19, decca::hardware::kSwitchOnOff);
    TEST_ASSERT_EQUAL_UINT8(23, decca::hardware::kButtonVhf);
    TEST_ASSERT_EQUAL_UINT8(21, decca::hardware::kDisplaySda);
    TEST_ASSERT_EQUAL_UINT8(22, decca::hardware::kDisplayScl);
    TEST_ASSERT_EQUAL_UINT8(25, decca::hardware::kDialLightingPwm);
}

void test_hardware_peripheral_configuration() {
    TEST_ASSERT_EQUAL_UINT8(12, decca::hardware::kAdcResolutionBits);
    TEST_ASSERT_EQUAL_UINT8(0, decca::hardware::kDialLightingPwmChannel);
    TEST_ASSERT_EQUAL_UINT32(5000,
                             decca::hardware::kDialLightingPwmFrequencyHz);
    TEST_ASSERT_EQUAL_UINT8(
        8, decca::hardware::kDialLightingPwmResolutionBits);
}

// init() must be callable and return cleanly.
void test_hardware_init_is_callable() {
    decca::hardware::init();
    TEST_PASS();
}

void runAll() {
    RUN_TEST(test_hardware_pin_map_contract);
    RUN_TEST(test_hardware_peripheral_configuration);
    RUN_TEST(test_hardware_init_is_callable);
}

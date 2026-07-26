/**
 * @file    test_hardware.cpp
 * @brief   Interface smoke tests for the hardware module.
 *
 * These confirm the proposed pin-map contract and that the module entry point
 * is callable. Expand into pin-mode/ADC/PWM behaviour tests as init() gains
 * real logic.
 */

#include "unity_runner.h"

#include "hardware.h"

// Named constants must match the proposed map in docs/Wiring.md.
void test_hardware_proposed_pin_map() {
    TEST_ASSERT_EQUAL_UINT8(32, decca::hardware::kPotVolume);
    TEST_ASSERT_EQUAL_UINT8(33, decca::hardware::kPotBass);
    TEST_ASSERT_EQUAL_UINT8(34, decca::hardware::kPotTreble);
    TEST_ASSERT_EQUAL_UINT8(35, decca::hardware::kPotBalance);
    TEST_ASSERT_EQUAL_UINT8(19, decca::hardware::kSwitchOnOff);
    TEST_ASSERT_EQUAL_UINT8(21, decca::hardware::kDisplaySda);
    TEST_ASSERT_EQUAL_UINT8(22, decca::hardware::kDisplayScl);
    TEST_ASSERT_EQUAL_UINT8(25, decca::hardware::kDialLightingPwm);
}

// init() must be callable and return cleanly.
void test_hardware_init_is_callable() {
    decca::hardware::init();
    TEST_PASS();
}

void runAll() {
    RUN_TEST(test_hardware_proposed_pin_map);
    RUN_TEST(test_hardware_init_is_callable);
}

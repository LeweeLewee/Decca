/**
 * @file    test_hardware.cpp
 * @brief   Interface smoke tests for the hardware module.
 *
 * These confirm the pin-map contract and exercise the real
 * board-initialisation entry point.
 */

#include "unity_runner.h"

#include <cstddef>

#include "hardware.h"

namespace {

constexpr uint8_t kAssignedPins[] = {
    decca::hardware::kPotVolume,
    decca::hardware::kPotBass,
    decca::hardware::kPotTreble,
    decca::hardware::kPotBalance,
    decca::hardware::kSwitchOnOff,
    decca::hardware::kButtonVhf,
    decca::hardware::kSwitchStereoMono,
    decca::hardware::kDisplaySda,
    decca::hardware::kDisplayScl,
    decca::hardware::kDialLightingPwm,
};

constexpr std::size_t kAssignedPinCount =
    sizeof(kAssignedPins) / sizeof(kAssignedPins[0]);

constexpr bool assignedPinsAreUnique() {
    for (std::size_t first = 0; first < kAssignedPinCount; ++first) {
        for (std::size_t second = first + 1; second < kAssignedPinCount;
             ++second) {
            if (kAssignedPins[first] == kAssignedPins[second]) {
                return false;
            }
        }
    }
    return true;
}

constexpr bool isExcludedStrappingPin(uint8_t pin) {
    return pin == 0 || pin == 2 || pin == 5 || pin == 12 || pin == 15;
}

static_assert(assignedPinsAreUnique(), "duplicate GPIO assignment");
static_assert(!isExcludedStrappingPin(decca::hardware::kButtonVhf),
              "VHF input uses an excluded strapping pin");
static_assert(!isExcludedStrappingPin(decca::hardware::kSwitchStereoMono),
              "Stereo/Mono input uses an excluded strapping pin");

}  // namespace

// Named constants and their verification status must match docs/Wiring.md.
void test_hardware_pin_map_contract() {
    TEST_ASSERT_EQUAL_UINT8(32, decca::hardware::kPotVolume);
    TEST_ASSERT_EQUAL_UINT8(33, decca::hardware::kPotBass);
    TEST_ASSERT_EQUAL_UINT8(34, decca::hardware::kPotTreble);
    TEST_ASSERT_EQUAL_UINT8(35, decca::hardware::kPotBalance);
    TEST_ASSERT_EQUAL_UINT8(19, decca::hardware::kSwitchOnOff);
    TEST_ASSERT_EQUAL_UINT8(26, decca::hardware::kButtonVhf);
    TEST_ASSERT_EQUAL_UINT8(14, decca::hardware::kSwitchStereoMono);
    TEST_ASSERT_EQUAL_UINT8(21, decca::hardware::kDisplaySda);
    TEST_ASSERT_EQUAL_UINT8(22, decca::hardware::kDisplayScl);
    TEST_ASSERT_EQUAL_UINT8(25, decca::hardware::kDialLightingPwm);
}

void test_hardware_gpio_map_has_no_duplicates() {
    for (std::size_t first = 0; first < kAssignedPinCount; ++first) {
        for (std::size_t second = first + 1; second < kAssignedPinCount;
             ++second) {
            TEST_ASSERT_NOT_EQUAL(kAssignedPins[first], kAssignedPins[second]);
        }
    }
}

void test_hardware_peripheral_configuration() {
    TEST_ASSERT_EQUAL_UINT8(12, decca::hardware::kAdcResolutionBits);
    TEST_ASSERT_EQUAL_UINT8(0, decca::hardware::kDialLightingPwmChannel);
    TEST_ASSERT_EQUAL_UINT32(1000,
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
    RUN_TEST(test_hardware_gpio_map_has_no_duplicates);
    RUN_TEST(test_hardware_peripheral_configuration);
    RUN_TEST(test_hardware_init_is_callable);
}

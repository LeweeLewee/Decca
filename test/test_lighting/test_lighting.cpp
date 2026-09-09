/**
 * @file    test_lighting.cpp
 * @brief   Behavioural tests for immediate PWM dial illumination.
 */

#include "unity_runner.h"

#include "hardware.h"
#include "lighting.h"
#include "settings.h"

using decca::lighting::Zone;

namespace {

uint8_t g_lastChannel = 0;
uint32_t g_lastDuty = 0;
uint16_t g_writeCount = 0;

void captureDuty(uint8_t channel, uint32_t duty) {
    g_lastChannel = channel;
    g_lastDuty = duty;
    ++g_writeCount;
}

void startInjected() {
    g_lastChannel = 0;
    g_lastDuty = 999;
    g_writeCount = 0;

    decca::lighting::testing::setDutyWriter(captureDuty);
    decca::lighting::init();
}

}  // namespace

void test_lighting_physical_switch_snapshot() {
    decca::hardware::init();
    decca::lighting::testing::resetHooks();
    decca::lighting::init();
    constexpr uint8_t kCommissioningDuty =
        decca::settings::kDefaultDialBrightness;
    constexpr uint32_t kCommissioningHoldMs = 5000;

    decca::lighting::setBrightness(Zone::Dial, kCommissioningDuty);

    UnityPrint("LIGHTING_SNAPSHOT duty=");
    UnityPrintNumberUnsigned(decca::lighting::brightness(Zone::Dial));
    UNITY_PRINT_EOL();
    TEST_ASSERT_EQUAL_UINT8(kCommissioningDuty,
                            decca::lighting::brightness(Zone::Dial));
    delay(kCommissioningHoldMs);

    decca::lighting::setBrightness(Zone::Dial, 0);
    TEST_ASSERT_EQUAL_UINT8(0,
                            decca::lighting::brightness(Zone::Dial));
}

void test_lighting_init_applies_safe_off() {
    startInjected();

    TEST_ASSERT_EQUAL_UINT8(0, decca::lighting::brightness(Zone::Dial));
    TEST_ASSERT_EQUAL_UINT32(0, g_lastDuty);
    TEST_ASSERT_EQUAL_UINT16(1, g_writeCount);
}

void test_lighting_applies_on_brightness_immediately() {
    startInjected();

    decca::lighting::setBrightness(Zone::Dial, 217);

    TEST_ASSERT_EQUAL_UINT8(217, decca::lighting::brightness(Zone::Dial));
    TEST_ASSERT_EQUAL_UINT32(217, g_lastDuty);
    TEST_ASSERT_EQUAL_UINT8(decca::hardware::kDialLightingPwmChannel,
                            g_lastChannel);
    TEST_ASSERT_EQUAL_UINT16(2, g_writeCount);
}

void test_lighting_applies_off_brightness_immediately() {
    startInjected();
    decca::lighting::setBrightness(Zone::Dial, 217);

    decca::lighting::setBrightness(Zone::Dial, 0);

    TEST_ASSERT_EQUAL_UINT8(0, decca::lighting::brightness(Zone::Dial));
    TEST_ASSERT_EQUAL_UINT32(0, g_lastDuty);
    TEST_ASSERT_EQUAL_UINT16(3, g_writeCount);
}

void test_lighting_does_not_rewrite_unchanged_brightness() {
    startInjected();
    decca::lighting::setBrightness(Zone::Dial, 217);
    const uint16_t writesAtTarget = g_writeCount;

    decca::lighting::setBrightness(Zone::Dial, 217);

    TEST_ASSERT_EQUAL_UINT16(writesAtTarget, g_writeCount);
}

void test_lighting_ignores_invalid_zone() {
    startInjected();
    const Zone invalid = static_cast<Zone>(99);

    decca::lighting::setBrightness(invalid, 255);

    TEST_ASSERT_EQUAL_UINT8(0, decca::lighting::brightness(Zone::Dial));
    TEST_ASSERT_EQUAL_UINT8(0, decca::lighting::brightness(invalid));
    TEST_ASSERT_EQUAL_UINT16(1, g_writeCount);
}

void runAll() {
    RUN_TEST(test_lighting_physical_switch_snapshot);
    RUN_TEST(test_lighting_init_applies_safe_off);
    RUN_TEST(test_lighting_applies_on_brightness_immediately);
    RUN_TEST(test_lighting_applies_off_brightness_immediately);
    RUN_TEST(test_lighting_does_not_rewrite_unchanged_brightness);
    RUN_TEST(test_lighting_ignores_invalid_zone);
}

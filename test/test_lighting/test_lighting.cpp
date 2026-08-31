/**
 * @file    test_lighting.cpp
 * @brief   Behavioural tests for PWM dial illumination and fades.
 */

#include "unity_runner.h"

#include "hardware.h"
#include "lighting.h"
#include "settings.h"

using decca::lighting::Zone;

namespace {

uint32_t g_nowMs = 0;
uint8_t g_lastChannel = 0;
uint32_t g_lastDuty = 0;
uint16_t g_writeCount = 0;

uint32_t fakeTime() {
    return g_nowMs;
}

void captureDuty(uint8_t channel, uint32_t duty) {
    g_lastChannel = channel;
    g_lastDuty = duty;
    ++g_writeCount;
}

void startInjected(uint8_t persistedBrightness = 0) {
    g_nowMs = 100;
    g_lastChannel = 0;
    g_lastDuty = 999;
    g_writeCount = 0;

    decca::settings::State state = decca::settings::get();
    state.dial = persistedBrightness;
    decca::settings::set(state);

    decca::lighting::testing::setTimeProvider(fakeTime);
    decca::lighting::testing::setDutyWriter(captureDuty);
    decca::lighting::init();
}

void advance(uint32_t elapsedMs) {
    g_nowMs += elapsedMs;
    decca::lighting::update();
}

}  // namespace

void test_lighting_physical_fade_snapshot() {
    decca::hardware::init();
    decca::lighting::testing::resetHooks();
    decca::settings::State state = decca::settings::get();
    state.dial = 0;
    decca::settings::set(state);
    decca::lighting::init();
    constexpr uint8_t kCommissioningDuty = 64;
    constexpr uint32_t kCommissioningHoldMs = 5000;
    decca::lighting::setBrightness(Zone::Dial, kCommissioningDuty);

    for (uint8_t step = 0; step < kCommissioningDuty; ++step) {
        delay(decca::lighting::kFadeStepIntervalMs);
        decca::lighting::update();
    }

    UnityPrint("LIGHTING_SNAPSHOT duty=");
    UnityPrintNumberUnsigned(decca::lighting::brightness(Zone::Dial));
    UNITY_PRINT_EOL();
    TEST_ASSERT_EQUAL_UINT8(kCommissioningDuty,
                            decca::lighting::brightness(Zone::Dial));
    delay(kCommissioningHoldMs);

    decca::lighting::setBrightness(Zone::Dial, 0);
    for (uint8_t step = 0; step < kCommissioningDuty; ++step) {
        delay(decca::lighting::kFadeStepIntervalMs);
        decca::lighting::update();
    }
    TEST_ASSERT_EQUAL_UINT8(0,
                            decca::lighting::brightness(Zone::Dial));
}

void test_lighting_init_applies_safe_off_before_persisted_target() {
    startInjected(80);

    TEST_ASSERT_EQUAL_UINT8(0, decca::lighting::brightness(Zone::Dial));
    TEST_ASSERT_EQUAL_UINT8(80,
                            decca::lighting::targetBrightness(Zone::Dial));
    TEST_ASSERT_EQUAL_UINT32(0, g_lastDuty);
    TEST_ASSERT_EQUAL_UINT16(1, g_writeCount);
}

void test_lighting_waits_for_non_blocking_fade_interval() {
    startInjected();
    decca::lighting::setBrightness(Zone::Dial, 20);

    advance(decca::lighting::kFadeStepIntervalMs - 1);

    TEST_ASSERT_EQUAL_UINT8(0, decca::lighting::brightness(Zone::Dial));
    TEST_ASSERT_EQUAL_UINT16(1, g_writeCount);
}

void test_lighting_fades_up_by_elapsed_steps() {
    startInjected();
    decca::lighting::setBrightness(Zone::Dial, 20);

    advance(5 * decca::lighting::kFadeStepIntervalMs);

    TEST_ASSERT_EQUAL_UINT8(5, decca::lighting::brightness(Zone::Dial));
    TEST_ASSERT_EQUAL_UINT32(5, g_lastDuty);
    TEST_ASSERT_EQUAL_UINT8(decca::hardware::kDialLightingPwmChannel,
                            g_lastChannel);
}

void test_lighting_stops_exactly_at_target() {
    startInjected();
    decca::lighting::setBrightness(Zone::Dial, 3);

    advance(20 * decca::lighting::kFadeStepIntervalMs);

    TEST_ASSERT_EQUAL_UINT8(3, decca::lighting::brightness(Zone::Dial));
    TEST_ASSERT_EQUAL_UINT32(3, g_lastDuty);
    const uint16_t writesAtTarget = g_writeCount;
    advance(1000);
    TEST_ASSERT_EQUAL_UINT16(writesAtTarget, g_writeCount);
}

void test_lighting_fades_down() {
    startInjected();
    decca::lighting::setBrightness(Zone::Dial, 10);
    advance(10 * decca::lighting::kFadeStepIntervalMs);
    decca::lighting::setBrightness(Zone::Dial, 4);

    advance(3 * decca::lighting::kFadeStepIntervalMs);

    TEST_ASSERT_EQUAL_UINT8(7, decca::lighting::brightness(Zone::Dial));
    TEST_ASSERT_EQUAL_UINT32(7, g_lastDuty);
}

void test_lighting_ignores_invalid_zone() {
    startInjected();
    const Zone invalid = static_cast<Zone>(99);

    decca::lighting::setBrightness(invalid, 255);

    TEST_ASSERT_EQUAL_UINT8(0, decca::lighting::targetBrightness(Zone::Dial));
    TEST_ASSERT_EQUAL_UINT8(0, decca::lighting::brightness(invalid));
}

void runAll() {
    RUN_TEST(test_lighting_physical_fade_snapshot);
    RUN_TEST(test_lighting_init_applies_safe_off_before_persisted_target);
    RUN_TEST(test_lighting_waits_for_non_blocking_fade_interval);
    RUN_TEST(test_lighting_fades_up_by_elapsed_steps);
    RUN_TEST(test_lighting_stops_exactly_at_target);
    RUN_TEST(test_lighting_fades_down);
    RUN_TEST(test_lighting_ignores_invalid_zone);
}

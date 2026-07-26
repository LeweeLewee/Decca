/**
 * @file    test_lighting.cpp
 * @brief   Interface smoke tests for the lighting module.
 *
 * These confirm the module links and its brightness interface accepts the full
 * range without faulting. As fades/effects land, add tests that step update()
 * over time and assert the output approaches its target.
 */

#include "unity_runner.h"

#include "lighting.h"

using decca::lighting::Zone;

// Dial brightness must be settable across the full range.
void test_lighting_set_brightness_callable() {
    decca::lighting::init();
    decca::lighting::setBrightness(Zone::Dial, 0);
    decca::lighting::setBrightness(Zone::Dial, 255);
    decca::lighting::update();
    TEST_PASS();
}

void runAll() {
    RUN_TEST(test_lighting_set_brightness_callable);
}

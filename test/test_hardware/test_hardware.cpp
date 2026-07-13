/**
 * @file    test_hardware.cpp
 * @brief   Interface smoke tests for the hardware module.
 *
 * At the foundation stage these confirm the module links and its entry point is
 * callable without faulting. Expand into behavioural tests (pin modes, ADC/PWM
 * configuration) as hardware::init() gains real logic.
 */

#include "unity_runner.h"

#include "hardware.h"

// init() must be callable and return cleanly.
void test_hardware_init_is_callable() {
    decca::hardware::init();
    TEST_PASS();
}

void runAll() {
    RUN_TEST(test_hardware_init_is_callable);
}

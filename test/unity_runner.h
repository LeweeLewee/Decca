/**
 * @file    unity_runner.h
 * @brief   Shared boilerplate for on-target Unity test suites.
 *
 * PlatformIO's embedded (Arduino framework) Unity tests each provide their own
 * setup()/loop(). This header supplies the common runner so each suite only has
 * to define its test functions and a RUN_ALL() macro body.
 *
 * Usage in a suite (test_<module>/test_<module>.cpp):
 *
 *     #include "unity_runner.h"
 *     void test_foo() { TEST_ASSERT_TRUE(...); }
 *     void runAll()   { RUN_TEST(test_foo); }
 *
 * The setup()/loop() below are compiled once per suite because this header is
 * included by exactly one .cpp in each test folder.
 */

#pragma once

#include <Arduino.h>
#include <unity.h>

// Each suite defines these.
void runAll();

void setUp(void) {}
void tearDown(void) {}

void setup() {
    // Allow the USB/serial link to settle before the report is emitted.
    delay(2000);
    UNITY_BEGIN();
    runAll();
    UNITY_END();
}

void loop() {}

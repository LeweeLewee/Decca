/**
 * @file    test_pots.cpp
 * @brief   Tests for the pots module (filtered analogue input).
 *
 * The value range check will become meaningful once ADC sampling and filtering
 * land; for now it asserts the stub returns an in-range default and that the
 * interface is callable.
 */

#include "unity_runner.h"

#include "pots.h"

using decca::pots::Pot;

// Values must always fall within the documented normalised range (0–1000).
void test_pots_value_in_range() {
    decca::pots::init();
    decca::pots::update();
    uint16_t v = decca::pots::value(Pot::Volume);
    TEST_ASSERT_LESS_OR_EQUAL_UINT16(1000, v);
}

void runAll() {
    RUN_TEST(test_pots_value_in_range);
}

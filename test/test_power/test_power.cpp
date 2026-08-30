/** @file test_power.cpp @brief Logical system-power state tests. */
#include "unity_runner.h"

#include "power.h"

using decca::power::State;

void test_power_initialises_on_from_closed_switch() {
    decca::power::init(true);

    TEST_ASSERT_EQUAL(static_cast<int>(State::On),
                      static_cast<int>(decca::power::state()));
    TEST_ASSERT_TRUE(decca::power::isOn());
}

void test_power_initialises_standby_from_open_switch() {
    decca::power::init(false);

    TEST_ASSERT_EQUAL(static_cast<int>(State::Standby),
                      static_cast<int>(decca::power::state()));
    TEST_ASSERT_FALSE(decca::power::isOn());
}

void test_power_reports_transition_to_on_once() {
    decca::power::init(false);

    TEST_ASSERT_TRUE(decca::power::update(true));
    TEST_ASSERT_TRUE(decca::power::isOn());
    TEST_ASSERT_FALSE(decca::power::update(true));
}

void test_power_reports_transition_to_standby_once() {
    decca::power::init(true);

    TEST_ASSERT_TRUE(decca::power::update(false));
    TEST_ASSERT_FALSE(decca::power::isOn());
    TEST_ASSERT_FALSE(decca::power::update(false));
}

void test_power_follows_repeated_latched_switch_changes() {
    decca::power::init(false);

    TEST_ASSERT_TRUE(decca::power::update(true));
    TEST_ASSERT_TRUE(decca::power::update(false));
    TEST_ASSERT_TRUE(decca::power::update(true));
    TEST_ASSERT_EQUAL(static_cast<int>(State::On),
                      static_cast<int>(decca::power::state()));
}

void runAll() {
    RUN_TEST(test_power_initialises_on_from_closed_switch);
    RUN_TEST(test_power_initialises_standby_from_open_switch);
    RUN_TEST(test_power_reports_transition_to_on_once);
    RUN_TEST(test_power_reports_transition_to_standby_once);
    RUN_TEST(test_power_follows_repeated_latched_switch_changes);
}

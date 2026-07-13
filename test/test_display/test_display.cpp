/**
 * @file    test_display.cpp
 * @brief   Interface smoke tests for the display module.
 *
 * The OLED cannot be asserted on directly here, so these confirm the module
 * links and its interface is callable without faulting. As rendering lands,
 * consider a fake/headless panel backend to assert on framebuffer contents.
 */

#include "unity_runner.h"

#include "display.h"

// init(), update() and showStatus() must all be callable.
void test_display_interface_callable() {
    decca::display::init();
    decca::display::update();
    decca::display::showStatus("test");
    TEST_PASS();
}

void runAll() {
    RUN_TEST(test_display_interface_callable);
}

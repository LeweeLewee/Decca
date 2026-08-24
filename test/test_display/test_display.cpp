/**
 * @file    test_display.cpp
 * @brief   Behavioural and physical tests for the SH1106 display module.
 */

#include "unity_runner.h"

#include <cstring>

#include "display.h"
#include "hardware.h"

using decca::display::FrameKind;
using decca::display::PowerState;
using decca::display::ViewState;

namespace {

uint32_t g_nowMs = 0;
bool g_beginResult = true;
uint16_t g_frameCount = 0;
FrameKind g_lastKind = FrameKind::Startup;
ViewState g_lastState;
char g_lastMessage[decca::display::kMessageCapacity + 1]{};

uint32_t fakeTime() {
    return g_nowMs;
}

bool fakeBegin() {
    return g_beginResult;
}

void captureFrame(const decca::display::testing::Frame& frame) {
    ++g_frameCount;
    g_lastKind = frame.kind;
    g_lastState = frame.state;
    std::strncpy(g_lastMessage,
                 frame.message,
                 decca::display::kMessageCapacity);
    g_lastMessage[decca::display::kMessageCapacity] = '\0';
}

void startInjected(bool beginResult = true) {
    g_nowMs = 100;
    g_beginResult = beginResult;
    g_frameCount = 0;
    g_lastKind = FrameKind::Startup;
    g_lastState = ViewState{};
    g_lastMessage[0] = '\0';
    decca::display::testing::setTimeProvider(fakeTime);
    decca::display::testing::setPanelBegin(fakeBegin);
    decca::display::testing::setFrameWriter(captureFrame);
    decca::display::init();
}

void finishStartup() {
    g_nowMs += decca::display::kStartupDurationMs;
    decca::display::update();
}

}  // namespace

void test_display_physical_sh1106_snapshot() {
    decca::hardware::init();
    decca::display::testing::resetHooks();
    decca::display::init();

    UnityPrint("DISPLAY_SNAPSHOT controller=SH1106 address=0x3C ready=");
    UnityPrintNumberUnsigned(decca::display::ready() ? 1 : 0);
    UNITY_PRINT_EOL();
    TEST_ASSERT_TRUE(decca::display::ready());

    ViewState state;
    state.power = PowerState::On;
    state.source = decca::settings::Source::Gram;
    state.volume = 750;
    state.bass = 500;
    state.treble = 500;
    state.balance = 500;
    decca::display::setState(state);
    delay(decca::display::kStartupDurationMs);
    decca::display::update();
}

void test_display_init_renders_non_blocking_startup() {
    startInjected();

    TEST_ASSERT_TRUE(decca::display::ready());
    TEST_ASSERT_EQUAL_UINT16(1, g_frameCount);
    TEST_ASSERT_EQUAL(static_cast<int>(FrameKind::Startup),
                      static_cast<int>(g_lastKind));

    g_nowMs += decca::display::kStartupDurationMs - 1;
    decca::display::update();
    TEST_ASSERT_EQUAL_UINT16(1, g_frameCount);

    ++g_nowMs;
    decca::display::update();
    TEST_ASSERT_EQUAL_UINT16(2, g_frameCount);
    TEST_ASSERT_EQUAL(static_cast<int>(FrameKind::Dashboard),
                      static_cast<int>(g_lastKind));
}

void test_display_dashboard_carries_on_source_and_controls() {
    startInjected();
    ViewState state;
    state.power = PowerState::On;
    state.source = decca::settings::Source::Mw;
    state.volume = 1000;
    state.bass = 600;
    state.treble = 400;
    state.balance = 500;
    decca::display::setState(state);
    finishStartup();

    TEST_ASSERT_EQUAL(static_cast<int>(FrameKind::Dashboard),
                      static_cast<int>(g_lastKind));
    TEST_ASSERT_EQUAL(static_cast<int>(PowerState::On),
                      static_cast<int>(g_lastState.power));
    TEST_ASSERT_EQUAL(static_cast<int>(decca::settings::Source::Mw),
                      static_cast<int>(g_lastState.source));
    TEST_ASSERT_EQUAL_UINT16(1000, g_lastState.volume);
    TEST_ASSERT_EQUAL_UINT16(600, g_lastState.bass);
    TEST_ASSERT_EQUAL_UINT16(400, g_lastState.treble);
    TEST_ASSERT_EQUAL_UINT16(500, g_lastState.balance);
}

void test_display_clamps_values_and_avoids_redundant_redraws() {
    startInjected();
    finishStartup();
    ViewState state;
    state.volume = 1500;
    state.bass = 1001;
    decca::display::setState(state);
    decca::display::update();

    TEST_ASSERT_EQUAL_UINT16(1000, g_lastState.volume);
    TEST_ASSERT_EQUAL_UINT16(1000, g_lastState.bass);
    const uint16_t framesAfterChange = g_frameCount;
    decca::display::setState(state);
    decca::display::update();
    TEST_ASSERT_EQUAL_UINT16(framesAfterChange, g_frameCount);
}

void test_display_status_expires_back_to_dashboard() {
    startInjected();
    finishStartup();
    decca::display::showStatus("Volume 42");
    decca::display::update();

    TEST_ASSERT_EQUAL(static_cast<int>(FrameKind::Status),
                      static_cast<int>(g_lastKind));
    TEST_ASSERT_EQUAL_STRING("Volume 42", g_lastMessage);

    g_nowMs += decca::display::kStatusDurationMs;
    decca::display::update();
    TEST_ASSERT_EQUAL(static_cast<int>(FrameKind::Dashboard),
                      static_cast<int>(g_lastKind));
}

void test_display_renders_diagnostics_and_sw_unavailable() {
    startInjected();
    finishStartup();
    decca::display::showDiagnostic("I2C CHECK");
    decca::display::update();
    TEST_ASSERT_EQUAL(static_cast<int>(FrameKind::Diagnostic),
                      static_cast<int>(g_lastKind));
    TEST_ASSERT_EQUAL_STRING("I2C CHECK", g_lastMessage);

    decca::display::showSwUnavailable();
    decca::display::update();
    TEST_ASSERT_EQUAL(static_cast<int>(FrameKind::Status),
                      static_cast<int>(g_lastKind));
    TEST_ASSERT_EQUAL_STRING("SW: NO FUNCTION", g_lastMessage);
}

void test_display_begin_failure_is_safe() {
    startInjected(false);

    TEST_ASSERT_FALSE(decca::display::ready());
    TEST_ASSERT_EQUAL_UINT16(0, g_frameCount);
    decca::display::showStatus("ignored safely");
    decca::display::update();
    TEST_ASSERT_EQUAL_UINT16(0, g_frameCount);
}

void runAll() {
    RUN_TEST(test_display_physical_sh1106_snapshot);
    RUN_TEST(test_display_init_renders_non_blocking_startup);
    RUN_TEST(test_display_dashboard_carries_on_source_and_controls);
    RUN_TEST(test_display_clamps_values_and_avoids_redundant_redraws);
    RUN_TEST(test_display_status_expires_back_to_dashboard);
    RUN_TEST(test_display_renders_diagnostics_and_sw_unavailable);
    RUN_TEST(test_display_begin_failure_is_safe);
}

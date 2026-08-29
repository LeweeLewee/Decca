/**
 * @file    test_display.cpp
 * @brief   Behavioural and physical tests for the SH1106 display module.
 */

#include "unity_runner.h"

#include <cstring>

#include "display.h"
#include "hardware.h"

using decca::display::Control;
using decca::display::FrameKind;
using decca::display::PowerState;
using decca::display::ViewState;

namespace {

uint32_t g_nowMs = 0;
bool g_beginResult = true;
uint16_t g_frameCount = 0;
FrameKind g_lastKind = FrameKind::Startup;
Control g_lastControl = Control::Volume;
uint16_t g_lastControlValue = 0;
uint8_t g_lastStartupFrame = 0;
ViewState g_lastState;
char g_lastFunction[decca::display::kFunctionCapacity + 1]{};
char g_lastTitle[decca::display::kTitleCapacity + 1]{};
char g_lastArtist[decca::display::kArtistCapacity + 1]{};
char g_lastMessage[decca::display::kMessageCapacity + 1]{};

template <size_t Capacity>
void captureText(char (&destination)[Capacity], const char* source) {
    std::strncpy(destination, source == nullptr ? "" : source, Capacity - 1U);
    destination[Capacity - 1U] = '\0';
}

uint32_t fakeTime() {
    return g_nowMs;
}

bool fakeBegin() {
    return g_beginResult;
}

void captureFrame(const decca::display::testing::Frame& frame) {
    ++g_frameCount;
    g_lastKind = frame.kind;
    g_lastControl = frame.control;
    g_lastControlValue = frame.controlValue;
    g_lastStartupFrame = frame.startupFrame;
    g_lastState = frame.state;
    captureText(g_lastFunction, frame.state.functionName);
    captureText(g_lastTitle, frame.state.title);
    captureText(g_lastArtist, frame.state.artist);
    captureText(g_lastMessage, frame.message);
    g_lastState.functionName = g_lastFunction;
    g_lastState.title = g_lastTitle;
    g_lastState.artist = g_lastArtist;
}

void startInjected(bool beginResult = true) {
    g_nowMs = 100;
    g_beginResult = beginResult;
    g_frameCount = 0;
    g_lastKind = FrameKind::Startup;
    g_lastControl = Control::Volume;
    g_lastControlValue = 0;
    g_lastStartupFrame = 0;
    g_lastState = ViewState{};
    g_lastFunction[0] = '\0';
    g_lastTitle[0] = '\0';
    g_lastArtist[0] = '\0';
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
    state.source = decca::settings::Source::Vinyl;
    state.volume = 750;
    state.bass = 500;
    state.treble = 500;
    state.balance = 500;
    state.functionName = "VINYL";
    decca::display::setState(state);

    for (uint8_t frame = 1; frame < decca::display::kStartupFrameCount;
         ++frame) {
        delay(decca::display::kStartupFrameIntervalMs);
        decca::display::update();
    }
    delay(decca::display::kStartupFrameIntervalMs);
    decca::display::update();
}

void test_display_animates_startup_without_blocking() {
    startInjected();

    TEST_ASSERT_TRUE(decca::display::ready());
    TEST_ASSERT_EQUAL_UINT16(1, g_frameCount);
    TEST_ASSERT_EQUAL(static_cast<int>(FrameKind::Startup),
                      static_cast<int>(g_lastKind));
    TEST_ASSERT_EQUAL_UINT8(0, g_lastStartupFrame);

    for (uint8_t frame = 1; frame < decca::display::kStartupFrameCount;
         ++frame) {
        g_nowMs += decca::display::kStartupFrameIntervalMs;
        decca::display::update();
        TEST_ASSERT_EQUAL(static_cast<int>(FrameKind::Startup),
                          static_cast<int>(g_lastKind));
        TEST_ASSERT_EQUAL_UINT8(frame, g_lastStartupFrame);
    }

    g_nowMs += decca::display::kStartupFrameIntervalMs;
    decca::display::update();
    TEST_ASSERT_EQUAL_UINT16(decca::display::kStartupFrameCount + 1U,
                            g_frameCount);
    TEST_ASSERT_EQUAL(static_cast<int>(FrameKind::Dashboard),
                      static_cast<int>(g_lastKind));
}

void test_display_dashboard_carries_function_and_controls() {
    startInjected();
    ViewState state;
    state.power = PowerState::On;
    state.source = decca::settings::Source::Vinyl;
    state.volume = 1000;
    state.bass = 600;
    state.treble = 400;
    state.balance = 500;
    state.functionName = "VINYL";
    decca::display::setState(state);
    finishStartup();

    TEST_ASSERT_EQUAL(static_cast<int>(FrameKind::Dashboard),
                      static_cast<int>(g_lastKind));
    TEST_ASSERT_EQUAL(static_cast<int>(PowerState::On),
                      static_cast<int>(g_lastState.power));
    TEST_ASSERT_EQUAL(static_cast<int>(decca::settings::Source::Vinyl),
                      static_cast<int>(g_lastState.source));
    TEST_ASSERT_EQUAL_STRING("VINYL", g_lastFunction);
    TEST_ASSERT_EQUAL_UINT16(1000, g_lastState.volume);
    TEST_ASSERT_EQUAL_UINT16(600, g_lastState.bass);
    TEST_ASSERT_EQUAL_UINT16(400, g_lastState.treble);
    TEST_ASSERT_EQUAL_UINT16(500, g_lastState.balance);
}

void test_display_copies_and_clears_now_playing_metadata() {
    startInjected();
    char function[] = "BBC RADIO 2";
    char title[] = "Gimme Shelter";
    char artist[] = "The Rolling Stones";
    ViewState state;
    state.power = PowerState::On;
    state.source = decca::settings::Source::DigitalStreamer;
    state.functionName = function;
    state.title = title;
    state.artist = artist;
    state.playing = true;
    decca::display::setState(state);
    function[0] = 'X';
    title[0] = 'X';
    artist[0] = 'X';
    finishStartup();

    TEST_ASSERT_TRUE(g_lastState.playing);
    TEST_ASSERT_EQUAL_STRING("BBC RADIO 2", g_lastFunction);
    TEST_ASSERT_EQUAL_STRING("Gimme Shelter", g_lastTitle);
    TEST_ASSERT_EQUAL_STRING("The Rolling Stones", g_lastArtist);

    state.functionName = "BBC RADIO 2";
    state.title = nullptr;
    state.artist = nullptr;
    state.playing = false;
    decca::display::setState(state);
    decca::display::update();
    TEST_ASSERT_FALSE(g_lastState.playing);
    TEST_ASSERT_EQUAL_STRING("BBC RADIO 2", g_lastFunction);
    TEST_ASSERT_EQUAL_STRING("", g_lastTitle);
    TEST_ASSERT_EQUAL_STRING("", g_lastArtist);
}

void test_display_control_view_clamps_and_expires() {
    startInjected();
    finishStartup();
    decca::display::showControl(Control::Balance, 1500);
    decca::display::update();

    TEST_ASSERT_EQUAL(static_cast<int>(FrameKind::Control),
                      static_cast<int>(g_lastKind));
    TEST_ASSERT_EQUAL(static_cast<int>(Control::Balance),
                      static_cast<int>(g_lastControl));
    TEST_ASSERT_EQUAL_UINT16(1000, g_lastControlValue);

    g_nowMs += decca::display::kControlDurationMs - 1U;
    decca::display::update();
    TEST_ASSERT_EQUAL(static_cast<int>(FrameKind::Control),
                      static_cast<int>(g_lastKind));
    ++g_nowMs;
    decca::display::update();
    TEST_ASSERT_EQUAL(static_cast<int>(FrameKind::Dashboard),
                      static_cast<int>(g_lastKind));
}

void test_display_confirms_mapped_function_then_returns() {
    startInjected();
    ViewState state;
    state.power = PowerState::On;
    state.source = decca::settings::Source::DigitalStreamer;
    state.functionName = "DIGITAL STREAMER";
    decca::display::setState(state);
    finishStartup();
    decca::display::showFunction();
    decca::display::update();

    TEST_ASSERT_EQUAL(static_cast<int>(FrameKind::Function),
                      static_cast<int>(g_lastKind));
    TEST_ASSERT_EQUAL_STRING("DIGITAL STREAMER", g_lastFunction);
    TEST_ASSERT_EQUAL(static_cast<int>(decca::settings::Source::DigitalStreamer),
                      static_cast<int>(g_lastState.source));

    g_nowMs += decca::display::kStatusDurationMs;
    decca::display::update();
    TEST_ASSERT_EQUAL(static_cast<int>(FrameKind::Dashboard),
                      static_cast<int>(g_lastKind));
}

void test_display_clamps_text_and_avoids_redundant_redraws() {
    startInjected();
    finishStartup();
    ViewState state;
    state.volume = 1500;
    state.bass = 1001;
    state.functionName = "123456789012345678901234567890";
    decca::display::setState(state);
    decca::display::update();

    TEST_ASSERT_EQUAL_UINT16(1000, g_lastState.volume);
    TEST_ASSERT_EQUAL_UINT16(1000, g_lastState.bass);
    TEST_ASSERT_EQUAL_UINT8(decca::display::kFunctionCapacity,
                            std::strlen(g_lastFunction));
    const uint16_t framesAfterChange = g_frameCount;
    decca::display::setState(state);
    decca::display::update();
    TEST_ASSERT_EQUAL_UINT16(framesAfterChange, g_frameCount);
}

void test_display_status_expires_back_to_dashboard() {
    startInjected();
    finishStartup();
    decca::display::showStatus("SOURCE READY");
    decca::display::update();

    TEST_ASSERT_EQUAL(static_cast<int>(FrameKind::Status),
                      static_cast<int>(g_lastKind));
    TEST_ASSERT_EQUAL_STRING("SOURCE READY", g_lastMessage);

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
    decca::display::showControl(Control::Volume, 500);
    decca::display::showStatus("ignored safely");
    decca::display::update();
    TEST_ASSERT_EQUAL_UINT16(0, g_frameCount);
}

void runAll() {
    RUN_TEST(test_display_physical_sh1106_snapshot);
    RUN_TEST(test_display_animates_startup_without_blocking);
    RUN_TEST(test_display_dashboard_carries_function_and_controls);
    RUN_TEST(test_display_copies_and_clears_now_playing_metadata);
    RUN_TEST(test_display_control_view_clamps_and_expires);
    RUN_TEST(test_display_confirms_mapped_function_then_returns);
    RUN_TEST(test_display_clamps_text_and_avoids_redundant_redraws);
    RUN_TEST(test_display_status_expires_back_to_dashboard);
    RUN_TEST(test_display_renders_diagnostics_and_sw_unavailable);
    RUN_TEST(test_display_begin_failure_is_safe);
}

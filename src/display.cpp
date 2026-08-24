/**
 * @file    display.cpp
 * @brief   Implementation of the SH1106 display module (see display.h).
 */

#include "display.h"

#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>
#include <Arduino.h>
#include <Wire.h>

#include <cstring>

namespace decca::display {
namespace {

Adafruit_SH1106G g_panel(kWidth, kHeight, &Wire, -1);
ViewState g_state;
bool g_ready = false;
bool g_dirty = false;
bool g_startupActive = false;
uint32_t g_startupStartedMs = 0;
FrameKind g_messageKind = FrameKind::Status;
char g_message[kMessageCapacity + 1]{};
uint32_t g_messageExpiresMs = 0;

#ifdef PIO_UNIT_TESTING
testing::TimeProvider g_timeProvider = nullptr;
testing::PanelBegin g_panelBegin = nullptr;
testing::FrameWriter g_frameWriter = nullptr;
#endif

uint32_t nowMs() {
#ifdef PIO_UNIT_TESTING
    if (g_timeProvider != nullptr) {
        return g_timeProvider();
    }
#endif
    return millis();
}

bool timeReached(uint32_t now, uint32_t deadline) {
    return static_cast<int32_t>(now - deadline) >= 0;
}

bool beginPanel() {
#ifdef PIO_UNIT_TESTING
    if (g_panelBegin != nullptr) {
        return g_panelBegin();
    }
#endif
    return g_panel.begin(kI2cAddress, true);
}

const char* sourceName(settings::Source source) {
    switch (source) {
        case settings::Source::Vhf:
            return "VHF";
        case settings::Source::Mw:
            return "MW";
        case settings::Source::Lw:
            return "LW";
        case settings::Source::Gram:
            return "GRAM";
    }
    return "?";
}

uint8_t percent(uint16_t value) {
    return static_cast<uint8_t>((value + 5U) / 10U);
}

void renderStartup() {
    g_panel.clearDisplay();
    g_panel.setTextColor(SH110X_WHITE);
    g_panel.setTextWrap(false);
    g_panel.setTextSize(2);
    g_panel.setCursor(34, 17);
    g_panel.print("DECCA");
    g_panel.setTextSize(1);
    g_panel.setCursor(40, 42);
    g_panel.print("STARTING");
    g_panel.display();
}

void renderDashboard(const ViewState& state) {
    g_panel.clearDisplay();
    g_panel.setTextColor(SH110X_WHITE);
    g_panel.setTextWrap(false);

    if (state.power == PowerState::Standby) {
        g_panel.setTextSize(2);
        g_panel.setCursor(34, 15);
        g_panel.print("DECCA");
        g_panel.setTextSize(1);
        g_panel.setCursor(43, 42);
        g_panel.print("STANDBY");
        g_panel.display();
        return;
    }

    g_panel.setTextSize(2);
    g_panel.setCursor(0, 0);
    g_panel.print(sourceName(state.source));
    g_panel.setTextSize(1);
    g_panel.setCursor(110, 0);
    g_panel.print("ON");
    g_panel.drawFastHLine(0, 18, kWidth, SH110X_WHITE);

    g_panel.setCursor(0, 23);
    g_panel.print("VOL ");
    g_panel.print(percent(state.volume));
    g_panel.print('%');
    g_panel.setCursor(68, 23);
    g_panel.print("BASS ");
    g_panel.print(percent(state.bass));

    g_panel.setCursor(0, 39);
    g_panel.print("TREB ");
    g_panel.print(percent(state.treble));
    g_panel.setCursor(68, 39);
    g_panel.print("BAL  ");
    g_panel.print(percent(state.balance));
    g_panel.display();
}

void renderMessage(FrameKind kind, const char* message) {
    g_panel.clearDisplay();
    g_panel.setTextColor(SH110X_WHITE);
    g_panel.setTextSize(1);
    g_panel.setTextWrap(false);
    g_panel.setCursor(0, 0);
    g_panel.print(kind == FrameKind::Diagnostic ? "DIAGNOSTIC" : "STATUS");
    g_panel.drawFastHLine(0, 10, kWidth, SH110X_WHITE);
    g_panel.setTextWrap(true);
    g_panel.setCursor(0, 18);
    g_panel.print(message);
    g_panel.display();
}

void writeFrame(FrameKind kind, const char* message = "") {
#ifdef PIO_UNIT_TESTING
    if (g_frameWriter != nullptr) {
        const testing::Frame frame{kind, g_state, message};
        g_frameWriter(frame);
        return;
    }
#endif
    switch (kind) {
        case FrameKind::Startup:
            renderStartup();
            break;
        case FrameKind::Dashboard:
            renderDashboard(g_state);
            break;
        case FrameKind::Status:
        case FrameKind::Diagnostic:
            renderMessage(kind, message);
            break;
    }
}

bool statesEqual(const ViewState& lhs, const ViewState& rhs) {
    return lhs.power == rhs.power && lhs.source == rhs.source &&
           lhs.volume == rhs.volume && lhs.bass == rhs.bass &&
           lhs.treble == rhs.treble && lhs.balance == rhs.balance;
}

ViewState clamped(const ViewState& state) {
    ViewState result = state;
    if (result.volume > kControlMax) {
        result.volume = kControlMax;
    }
    if (result.bass > kControlMax) {
        result.bass = kControlMax;
    }
    if (result.treble > kControlMax) {
        result.treble = kControlMax;
    }
    if (result.balance > kControlMax) {
        result.balance = kControlMax;
    }
    return result;
}

void setMessage(FrameKind kind, const char* message, uint32_t durationMs) {
    if (message == nullptr || message[0] == '\0') {
        return;
    }
    std::strncpy(g_message, message, kMessageCapacity);
    g_message[kMessageCapacity] = '\0';
    g_messageKind = kind;
    g_messageExpiresMs = nowMs() + durationMs;
    g_dirty = true;
}

}  // namespace

void init() {
    g_state = ViewState{};
    g_dirty = false;
    g_startupActive = false;
    g_message[0] = '\0';
    g_messageExpiresMs = 0;
    g_ready = beginPanel();
    if (!g_ready) {
        Serial.println("DISPLAY_ERROR SH1106 not found at 0x3C");
        return;
    }

    g_startupStartedMs = nowMs();
    g_startupActive = true;
    writeFrame(FrameKind::Startup);
}

void update() {
    if (!g_ready) {
        return;
    }

    const uint32_t now = nowMs();
    if (g_message[0] != '\0') {
        if (!timeReached(now, g_messageExpiresMs)) {
            if (g_dirty) {
                writeFrame(g_messageKind, g_message);
                g_dirty = false;
            }
            return;
        }
        g_message[0] = '\0';
        g_dirty = true;
    }

    if (g_startupActive) {
        if (!timeReached(now, g_startupStartedMs + kStartupDurationMs)) {
            return;
        }
        g_startupActive = false;
        g_dirty = true;
    }

    if (g_dirty) {
        writeFrame(FrameKind::Dashboard);
        g_dirty = false;
    }
}

bool ready() {
    return g_ready;
}

void setState(const ViewState& state) {
    const ViewState next = clamped(state);
    if (statesEqual(g_state, next)) {
        return;
    }
    g_state = next;
    g_dirty = true;
}

void showStatus(const char* message) {
    setMessage(FrameKind::Status, message, kStatusDurationMs);
}

void showDiagnostic(const char* message) {
    setMessage(FrameKind::Diagnostic, message, kDiagnosticDurationMs);
}

void showSwUnavailable() {
    showStatus("SW: NO FUNCTION");
}

#ifdef PIO_UNIT_TESTING
namespace testing {

void setTimeProvider(TimeProvider provider) {
    g_timeProvider = provider;
}

void setPanelBegin(PanelBegin begin) {
    g_panelBegin = begin;
}

void setFrameWriter(FrameWriter writer) {
    g_frameWriter = writer;
}

void resetHooks() {
    g_timeProvider = nullptr;
    g_panelBegin = nullptr;
    g_frameWriter = nullptr;
}

}  // namespace testing
#endif

}  // namespace decca::display

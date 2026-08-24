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
char g_functionName[kFunctionCapacity + 1]{};
char g_title[kTitleCapacity + 1]{};
char g_artist[kArtistCapacity + 1]{};
bool g_ready = false;
bool g_dirty = false;
bool g_startupActive = false;
uint32_t g_startupStartedMs = 0;
uint8_t g_startupFrame = 0;
bool g_transientActive = false;
FrameKind g_transientKind = FrameKind::Status;
Control g_transientControl = Control::Volume;
uint16_t g_transientControlValue = 0;
char g_message[kMessageCapacity + 1]{};
uint32_t g_transientExpiresMs = 0;

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

const char* textOrEmpty(const char* text) {
    return text == nullptr ? "" : text;
}

template <size_t Capacity>
void copyText(char (&destination)[Capacity], const char* source) {
    if (source == destination) {
        return;
    }
    std::strncpy(destination, textOrEmpty(source), Capacity - 1U);
    destination[Capacity - 1U] = '\0';
}

const char* buttonName(settings::Source source) {
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

const char* controlName(Control control) {
    switch (control) {
        case Control::Volume:
            return "VOLUME";
        case Control::Bass:
            return "BASS";
        case Control::Treble:
            return "TREBLE";
        case Control::Balance:
            return "BALANCE";
    }
    return "CONTROL";
}

const char* primaryFunction() {
    return g_functionName[0] == '\0' ? "LOCAL CONTROL" : g_functionName;
}

uint8_t percent(uint16_t value) {
    return static_cast<uint8_t>((value + 5U) / 10U);
}

uint16_t clampedControl(uint16_t value) {
    return value > kControlMax ? kControlMax : value;
}

void printClipped(const char* text, uint8_t maxCharacters) {
    char buffer[kTitleCapacity + 1]{};
    uint8_t limit = maxCharacters;
    if (limit > kTitleCapacity) {
        limit = kTitleCapacity;
    }
    std::strncpy(buffer, textOrEmpty(text), limit);
    buffer[limit] = '\0';
    g_panel.print(buffer);
}

void printButtonContext(settings::Source source) {
    g_panel.print('(');
    g_panel.print(buttonName(source));
    g_panel.print(" BUTTON)");
}

void renderStartup(uint8_t frame) {
    constexpr char kWordmark[] = "DECCA";
    char revealed[sizeof(kWordmark)]{};
    uint8_t characters = static_cast<uint8_t>(frame + 1U);
    if (characters > sizeof(kWordmark) - 1U) {
        characters = sizeof(kWordmark) - 1U;
    }
    std::memcpy(revealed, kWordmark, characters);

    g_panel.clearDisplay();
    g_panel.setTextColor(SH110X_WHITE);
    g_panel.setTextWrap(false);
    g_panel.setTextSize(2);
    const int16_t wordWidth = static_cast<int16_t>(characters) * 12;
    g_panel.setCursor((kWidth - wordWidth) / 2, 18);
    g_panel.print(revealed);

    const int16_t halfLine = static_cast<int16_t>(12U + (frame * 10U));
    g_panel.drawFastHLine(64 - halfLine, 43, halfLine * 2, SH110X_WHITE);
    if (frame + 1U == kStartupFrameCount) {
        g_panel.setTextSize(1);
        g_panel.setCursor(28, 50);
        g_panel.print("MUSIC CENTRE");
    }
    g_panel.display();
}

void renderPrimaryFunction(int16_t y) {
    const char* function = primaryFunction();
    const size_t length = std::strlen(function);
    if (length <= 10U) {
        g_panel.setTextSize(2);
        const int16_t width = static_cast<int16_t>(length) * 12;
        g_panel.setCursor((kWidth - width) / 2, y);
        g_panel.print(function);
        return;
    }

    g_panel.setTextSize(1);
    const size_t visibleLength = length > kFunctionCapacity
                                     ? kFunctionCapacity
                                     : length;
    const int16_t width = static_cast<int16_t>(visibleLength) * 6;
    g_panel.setCursor((kWidth - width) / 2, y + 4);
    printClipped(function, kFunctionCapacity);
}

void renderLocalDashboard() {
    renderPrimaryFunction(0);
    g_panel.setTextSize(1);
    g_panel.setCursor(0, 18);
    printButtonContext(g_state.source);
    g_panel.drawFastHLine(0, 28, kWidth, SH110X_WHITE);

    g_panel.setCursor(0, 34);
    g_panel.print("VOL ");
    g_panel.print(percent(g_state.volume));
    g_panel.print('%');
    g_panel.setCursor(68, 34);
    g_panel.print("BASS ");
    g_panel.print(percent(g_state.bass));

    g_panel.setCursor(0, 50);
    g_panel.print("TREB ");
    g_panel.print(percent(g_state.treble));
    g_panel.setCursor(68, 50);
    g_panel.print("BAL  ");
    g_panel.print(percent(g_state.balance));
}

void renderNowPlaying() {
    g_panel.setTextSize(1);
    g_panel.setCursor(0, 0);
    printClipped(primaryFunction(), 20);
    g_panel.setCursor(0, 10);
    printButtonContext(g_state.source);
    g_panel.drawFastHLine(0, 20, kWidth, SH110X_WHITE);

    g_panel.setCursor(0, 25);
    printClipped(g_title, 20);
    g_panel.setCursor(0, 39);
    printClipped(g_artist, 20);
    g_panel.setCursor(0, 54);
    g_panel.print("PLAYING");
}

void renderDashboard() {
    g_panel.clearDisplay();
    g_panel.setTextColor(SH110X_WHITE);
    g_panel.setTextWrap(false);

    if (g_state.power == PowerState::Standby) {
        g_panel.setTextSize(2);
        g_panel.setCursor(34, 15);
        g_panel.print("DECCA");
        g_panel.setTextSize(1);
        g_panel.setCursor(43, 42);
        g_panel.print("STANDBY");
        g_panel.display();
        return;
    }

    const bool hasMetadata = g_state.playing &&
                             (g_title[0] != '\0' || g_artist[0] != '\0');
    if (hasMetadata) {
        renderNowPlaying();
    } else {
        renderLocalDashboard();
    }
    g_panel.display();
}

void renderControl(Control control, uint16_t value) {
    g_panel.clearDisplay();
    g_panel.setTextColor(SH110X_WHITE);
    g_panel.setTextWrap(false);
    g_panel.setTextSize(2);
    const char* name = controlName(control);
    const int16_t nameWidth = static_cast<int16_t>(std::strlen(name)) * 12;
    g_panel.setCursor((kWidth - nameWidth) / 2, 4);
    g_panel.print(name);

    g_panel.drawRect(5, 27, 118, 14, SH110X_WHITE);
    const int16_t fillWidth = static_cast<int16_t>(
        (static_cast<uint32_t>(clampedControl(value)) * 114U) / kControlMax);
    if (fillWidth > 0) {
        g_panel.fillRect(7, 29, fillWidth, 10, SH110X_WHITE);
    }

    g_panel.setTextSize(1);
    g_panel.setCursor(52, 49);
    g_panel.print(percent(clampedControl(value)));
    g_panel.print('%');
    g_panel.display();
}

void renderFunctionConfirmation() {
    g_panel.clearDisplay();
    g_panel.setTextColor(SH110X_WHITE);
    g_panel.setTextWrap(false);
    g_panel.setTextSize(1);
    g_panel.setCursor(0, 0);
    g_panel.print("SELECTED");
    g_panel.drawFastHLine(0, 11, kWidth, SH110X_WHITE);
    renderPrimaryFunction(18);
    g_panel.setTextSize(1);
    g_panel.setCursor(0, 49);
    printButtonContext(g_state.source);
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

void writeFrame(FrameKind kind) {
#ifdef PIO_UNIT_TESTING
    if (g_frameWriter != nullptr) {
        const testing::Frame frame{kind,
                                   g_state,
                                   g_transientControl,
                                   g_transientControlValue,
                                   g_startupFrame,
                                   g_message};
        g_frameWriter(frame);
        return;
    }
#endif
    switch (kind) {
        case FrameKind::Startup:
            renderStartup(g_startupFrame);
            break;
        case FrameKind::Dashboard:
            renderDashboard();
            break;
        case FrameKind::Control:
            renderControl(g_transientControl, g_transientControlValue);
            break;
        case FrameKind::Function:
            renderFunctionConfirmation();
            break;
        case FrameKind::Status:
        case FrameKind::Diagnostic:
            renderMessage(kind, g_message);
            break;
    }
}

bool statesEqual(const ViewState& state) {
    return g_state.power == state.power && g_state.source == state.source &&
           g_state.volume == clampedControl(state.volume) &&
           g_state.bass == clampedControl(state.bass) &&
           g_state.treble == clampedControl(state.treble) &&
           g_state.balance == clampedControl(state.balance) &&
           g_state.playing == state.playing &&
           std::strncmp(g_functionName,
                        textOrEmpty(state.functionName),
                        kFunctionCapacity) == 0 &&
           std::strncmp(g_title,
                        textOrEmpty(state.title),
                        kTitleCapacity) == 0 &&
           std::strncmp(g_artist,
                        textOrEmpty(state.artist),
                        kArtistCapacity) == 0;
}

void copyState(const ViewState& state) {
    g_state.power = state.power;
    g_state.source = state.source;
    g_state.volume = clampedControl(state.volume);
    g_state.bass = clampedControl(state.bass);
    g_state.treble = clampedControl(state.treble);
    g_state.balance = clampedControl(state.balance);
    g_state.playing = state.playing;
    copyText(g_functionName, state.functionName);
    copyText(g_title, state.title);
    copyText(g_artist, state.artist);
    g_state.functionName = g_functionName;
    g_state.title = g_title;
    g_state.artist = g_artist;
}

void startTransient(FrameKind kind, uint32_t durationMs) {
    g_transientKind = kind;
    g_transientExpiresMs = nowMs() + durationMs;
    g_transientActive = true;
    g_dirty = true;
}

void setMessage(FrameKind kind, const char* message, uint32_t durationMs) {
    if (message == nullptr || message[0] == '\0') {
        return;
    }
    copyText(g_message, message);
    startTransient(kind, durationMs);
}

}  // namespace

void init() {
    g_state = ViewState{};
    g_functionName[0] = '\0';
    g_title[0] = '\0';
    g_artist[0] = '\0';
    g_state.functionName = g_functionName;
    g_state.title = g_title;
    g_state.artist = g_artist;
    g_dirty = false;
    g_startupActive = false;
    g_startupFrame = 0;
    g_transientActive = false;
    g_message[0] = '\0';
    g_transientExpiresMs = 0;
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
    if (g_transientActive) {
        if (!timeReached(now, g_transientExpiresMs)) {
            if (g_dirty) {
                writeFrame(g_transientKind);
                g_dirty = false;
            }
            return;
        }
        g_transientActive = false;
        g_message[0] = '\0';
        g_dirty = true;
    }

    if (g_startupActive) {
        const uint32_t elapsed = now - g_startupStartedMs;
        if (elapsed < kStartupDurationMs) {
            uint8_t frame = static_cast<uint8_t>(
                elapsed / kStartupFrameIntervalMs);
            if (frame >= kStartupFrameCount) {
                frame = kStartupFrameCount - 1U;
            }
            if (frame != g_startupFrame) {
                g_startupFrame = frame;
                writeFrame(FrameKind::Startup);
            }
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
    if (statesEqual(state)) {
        return;
    }
    copyState(state);
    g_dirty = true;
}

void showControl(Control control, uint16_t value) {
    g_transientControl = control;
    g_transientControlValue = clampedControl(value);
    g_message[0] = '\0';
    startTransient(FrameKind::Control, kControlDurationMs);
}

void showFunction() {
    g_message[0] = '\0';
    startTransient(FrameKind::Function, kStatusDurationMs);
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

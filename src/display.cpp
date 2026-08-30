/**
 * @file    display.cpp
 * @brief   Implementation of the SH1106 display module (see display.h).
 */

#include "display.h"

#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>
#include <Arduino.h>
#include <Wire.h>

#include <cstdio>
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
bool g_calibrationActive = false;
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

int16_t centredViewportX(int16_t width) {
    return static_cast<int16_t>(kViewportX) +
           (static_cast<int16_t>(kViewportWidth) - width) / 2;
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

void printCentredClipped(const char* text,
                         uint8_t maxCharacters,
                         int16_t y) {
    const size_t length = std::strlen(textOrEmpty(text));
    const uint8_t visibleLength = static_cast<uint8_t>(
        length > maxCharacters ? maxCharacters : length);
    g_panel.setCursor(centredViewportX(visibleLength * 6), y);
    printClipped(text, maxCharacters);
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
    g_panel.setCursor(centredViewportX(wordWidth), kContentTop);
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
        g_panel.setCursor(centredViewportX(width), y);
        g_panel.print(function);
        return;
    }

    g_panel.setTextSize(1);
    const size_t visibleLength = length > kFunctionCapacity
                                     ? kFunctionCapacity
                                     : length;
    const int16_t width = static_cast<int16_t>(visibleLength) * 6;
    g_panel.setCursor(centredViewportX(width), y + 4);
    printClipped(function, kFunctionCapacity);
}

void renderLocalDashboard() {
    g_panel.setTextSize(2);
    g_panel.setCursor(centredViewportX(60), kContentTop);
    g_panel.print("DECCA");
    g_panel.drawFastHLine(28, 43, 72, SH110X_WHITE);
    g_panel.setTextSize(1);
    g_panel.setCursor(28, 50);
    g_panel.print("MUSIC CENTRE");
}

void renderNowPlaying() {
    g_panel.setTextSize(1);
    printCentredClipped(g_title, 19, kContentTop);
    g_panel.drawFastHLine(18, 34, 92, SH110X_WHITE);
    printCentredClipped(g_artist, 19, 39);
    if (g_state.playing) {
        g_panel.fillTriangle(113, 51, 113, 59, 120, 55, SH110X_WHITE);
    } else {
        g_panel.fillRect(112, 51, 3, 8, SH110X_WHITE);
        g_panel.fillRect(118, 51, 3, 8, SH110X_WHITE);
    }
}

void renderDashboard() {
    g_panel.clearDisplay();
    g_panel.setTextColor(SH110X_WHITE);
    g_panel.setTextWrap(false);

    if (g_state.power == PowerState::Standby) {
        g_panel.setTextSize(2);
        g_panel.setCursor(centredViewportX(60), kContentTop);
        g_panel.print("DECCA");
        g_panel.setTextSize(1);
        g_panel.setCursor(centredViewportX(42), 50);
        g_panel.print("STANDBY");
        g_panel.display();
        return;
    }

    const bool hasMetadata = g_title[0] != '\0' || g_artist[0] != '\0';
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
    const char* name = controlName(control);
    g_panel.setTextSize(1);
    printCentredClipped(name, 19, kContentTop);

    char valueText[5]{};
    std::snprintf(valueText, sizeof(valueText), "%u%%",
                  static_cast<unsigned>(percent(clampedControl(value))));
    g_panel.setTextSize(2);
    const int16_t valueWidth =
        static_cast<int16_t>(std::strlen(valueText)) * 12;
    g_panel.setCursor(centredViewportX(valueWidth), 34);
    g_panel.print(valueText);

    g_panel.drawRect(10, 54, 108, 6, SH110X_WHITE);
    const int16_t fillWidth = static_cast<int16_t>(
        (static_cast<uint32_t>(clampedControl(value)) * 104U) / kControlMax);
    if (fillWidth > 0) {
        g_panel.fillRect(12, 56, fillWidth, 2, SH110X_WHITE);
    }
    g_panel.display();
}

void renderFunctionConfirmation() {
    g_panel.clearDisplay();
    g_panel.setTextColor(SH110X_WHITE);
    g_panel.setTextWrap(false);
    g_panel.setTextSize(1);
    printCentredClipped("SOURCE", 19, kContentTop);
    renderPrimaryFunction(38);
    g_panel.display();
}

void renderMessage(FrameKind kind, const char* message) {
    g_panel.clearDisplay();
    g_panel.setTextColor(SH110X_WHITE);
    g_panel.setTextSize(1);
    g_panel.setTextWrap(false);
    printCentredClipped(
        kind == FrameKind::Diagnostic ? "DIAGNOSTIC" : "STATUS",
        19,
        kContentTop);
    g_panel.drawFastHLine(18, 34, 92, SH110X_WHITE);
    g_panel.setTextWrap(true);
    g_panel.setCursor(7, 39);
    g_panel.print(message);
    g_panel.display();
}

void renderCalibration() {
    g_panel.clearDisplay();
    g_panel.setTextColor(SH110X_WHITE, SH110X_BLACK);
    g_panel.setTextWrap(false);

    // Three nested full-canvas borders expose clipping at 0, 2 and 4 pixels.
    g_panel.drawRect(0, 0, kWidth, kHeight, SH110X_WHITE);
    g_panel.drawRect(2, 2, kWidth - 4, kHeight - 4, SH110X_WHITE);
    g_panel.drawRect(4, 4, kWidth - 8, kHeight - 8, SH110X_WHITE);

    // Eight-pixel grid plus labelled major X coordinates locate the aperture.
    for (int16_t x = 8; x < kWidth; x += 8) {
        g_panel.drawFastVLine(x, 0, kHeight, SH110X_WHITE);
    }
    for (int16_t y = 8; y < kHeight; y += 8) {
        g_panel.drawFastHLine(0, y, kWidth, SH110X_WHITE);
    }

    g_panel.setTextSize(1);
    for (uint8_t y = 0; y < kHeight; y += 8) {
        g_panel.setCursor(10, static_cast<int16_t>(y) + 1);
        if (y < 10) {
            g_panel.print('0');
        }
        g_panel.print(y);
    }
    g_panel.setCursor(34, 27);
    g_panel.print("X32");
    g_panel.setCursor(58, 27);
    g_panel.print("X64");
    g_panel.setCursor(82, 27);
    g_panel.print("X96");

    // Asymmetric corner marks make a 180-degree orientation error obvious.
    g_panel.fillRect(0, 0, 4, 4, SH110X_WHITE);
    g_panel.fillRect(kWidth - 7, 0, 7, 3, SH110X_WHITE);
    g_panel.fillRect(0, kHeight - 7, 3, 7, SH110X_WHITE);
    g_panel.drawRect(kWidth - 7, kHeight - 7, 7, 7, SH110X_WHITE);
    g_panel.drawCircle(kWidth / 2, kHeight / 2, 4, SH110X_WHITE);
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
        case FrameKind::Calibration:
            renderCalibration();
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
    g_calibrationActive = false;
    g_startupFrame = 0;
    g_transientActive = false;
    g_message[0] = '\0';
    g_transientExpiresMs = 0;
    g_ready = beginPanel();
    if (!g_ready) {
        Serial.println("DISPLAY_ERROR SH1106 not found at 0x3C");
        return;
    }

    g_panel.setRotation(kPanelRotation);
    g_panel.setContrast(kPanelContrast);

    g_startupStartedMs = nowMs();
    g_startupActive = true;
    writeFrame(FrameKind::Startup);
}

void update() {
    if (!g_ready) {
        return;
    }

    const uint32_t now = nowMs();
    if (g_calibrationActive) {
        if (g_dirty) {
            writeFrame(FrameKind::Calibration);
            g_dirty = false;
        }
        return;
    }
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

void showCalibrationPattern() {
    if (!g_ready) {
        return;
    }
    g_calibrationActive = true;
    g_startupActive = false;
    g_transientActive = false;
    g_message[0] = '\0';
    g_dirty = true;
}

void hideCalibrationPattern() {
    if (!g_calibrationActive) {
        return;
    }
    g_calibrationActive = false;
    g_dirty = true;
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

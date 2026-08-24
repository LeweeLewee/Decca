/**
 * @file    display.h
 * @brief   SH1106 OLED display mounted behind the dial glass.
 *
 * display owns the 1.3-inch 128x64 I2C panel and everything drawn to it. It
 * renders state supplied by main and never reads input modules directly.
 *
 * Responsibility: render local state, animated startup, transient controls,
 *                 and Phase 2-ready mapped-function/metadata views; own
 *                 refresh timing and the OLED driver.
 * Depends on:      hardware (I2C), settings (source type/shared state).
 * Used by:         main; does not call input or lighting modules.
 */

#pragma once

#include <cstdint>

#include "settings.h"

namespace decca::display {

constexpr uint8_t kI2cAddress = 0x3C;
constexpr uint8_t kWidth = 128;
constexpr uint8_t kHeight = 64;
constexpr uint16_t kControlMax = 1000;
constexpr uint32_t kStartupDurationMs = 1000;
constexpr uint8_t kStartupFrameCount = 5;
constexpr uint32_t kStartupFrameIntervalMs =
    kStartupDurationMs / kStartupFrameCount;
constexpr uint32_t kControlDurationMs = 2000;
constexpr uint32_t kStatusDurationMs = 1500;
constexpr uint32_t kDiagnosticDurationMs = 3000;
constexpr uint8_t kMessageCapacity = 32;
constexpr uint8_t kFunctionCapacity = 20;
constexpr uint8_t kTitleCapacity = 32;
constexpr uint8_t kArtistCapacity = 24;

/** @brief Power state shown on the Phase 1 display. */
enum class PowerState : uint8_t {
    Standby,
    On,
};

/** @brief Front-panel control represented by a transient level view. */
enum class Control : uint8_t {
    Volume,
    Bass,
    Treble,
    Balance,
};

/**
 * @brief Coherent display snapshot supplied by the top-level coordinator.
 *
 * Control values use the pots module's normalised 0-1000 scale. Text pointers
 * may be null and are copied synchronously by setState() into fixed storage;
 * callers retain no lifetime obligation. Values above the control range and
 * text beyond the documented capacities are clamped/truncated.
 */
struct ViewState {
    PowerState power = PowerState::Standby;
    settings::Source source = settings::Source::Vhf;
    uint16_t volume = 0;
    uint16_t bass = 0;
    uint16_t treble = 0;
    uint16_t balance = 0;
    const char* functionName = nullptr;
    const char* title = nullptr;
    const char* artist = nullptr;
    bool playing = false;
};

/** @brief Semantic frame types used by the renderer and its test observer. */
enum class FrameKind : uint8_t {
    Startup,
    Dashboard,
    Control,
    Function,
    Status,
    Diagnostic,
};

/**
 * @brief Initialise the purchased SH1106 panel and render the startup frame.
 * @pre   hardware::init() has run and configured I2C on GPIO21/GPIO22.
 */
void init();

/**
 * @brief Redraw only when state changes or a transient expires. Non-blocking;
 *        call once per main loop.
 */
void update();

/** @brief Return whether the SH1106 acknowledged and initialised. */
bool ready();

/** @brief Supply a complete display snapshot; pointed-to text is copied. */
void setState(const ViewState& state);

/**
 * @brief Show a control name, level bar and percentage for 2 s.
 * @param control Control whose position changed.
 * @param value Normalised position; values above 1000 are clamped.
 */
void showControl(Control control, uint16_t value);

/** @brief Confirm the current mapped function and legacy button for 1.5 s. */
void showFunction();

/** @brief Show a short transient status message. */
void showStatus(const char* message);

/** @brief Show a longer transient diagnostic message. */
void showDiagnostic(const char* message);

/** @brief Present the retained SW position as unavailable in Phase 1. */
void showSwUnavailable();

#ifdef PIO_UNIT_TESTING
namespace testing {

struct Frame {
    FrameKind kind;
    ViewState state;
    Control control;
    uint16_t controlValue;
    uint8_t startupFrame;
    const char* message;
};

using TimeProvider = uint32_t (*)();
using PanelBegin = bool (*)();
using FrameWriter = void (*)(const Frame& frame);

/** Replace millis() with a deterministic provider. */
void setTimeProvider(TimeProvider provider);

/** Replace the physical SH1106 begin operation. */
void setPanelBegin(PanelBegin begin);

/** Observe semantic frames without writing to the physical OLED. */
void setFrameWriter(FrameWriter writer);

/** Restore real time and physical SH1106 operations. */
void resetHooks();

}  // namespace testing
#endif

}  // namespace decca::display

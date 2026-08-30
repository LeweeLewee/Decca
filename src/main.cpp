/** Phase 1 coordinator: logical power/display state plus continuous OTA. */
#include <Arduino.h>
#ifndef PIO_UNIT_TESTING
#include "buttons.h"
#include "display.h"
#include "hardware.h"
#include "ota.h"
#include "pots.h"
#include "power.h"

namespace {

decca::display::ViewState g_viewState;
decca::buttons::SourceMode g_sourceMode =
    decca::buttons::SourceMode::DigitalStreamer;
uint16_t g_potValues[4]{};
constexpr uint16_t kControlPresentationDeadband = 5;

constexpr decca::pots::Pot kPots[4] = {
    decca::pots::Pot::Volume,
    decca::pots::Pot::Bass,
    decca::pots::Pot::Treble,
    decca::pots::Pot::Balance,
};

constexpr decca::display::Control kControls[4] = {
    decca::display::Control::Volume,
    decca::display::Control::Bass,
    decca::display::Control::Treble,
    decca::display::Control::Balance,
};

void applySourceState(bool showConfirmation) {
    g_sourceMode = decca::buttons::sourceMode();
    const bool vinyl = g_sourceMode == decca::buttons::SourceMode::Vinyl;
    g_viewState.source = vinyl ? decca::settings::Source::Vinyl
                               : decca::settings::Source::DigitalStreamer;
    g_viewState.functionName = vinyl ? "VINYL" : "DIGITAL STREAMER";

    if (g_viewState.power == decca::display::PowerState::On) {
        decca::display::setState(g_viewState);
        if (showConfirmation) {
            decca::display::showFunction();
        }
    }

    Serial.print("[SOURCE] state=");
    Serial.println(vinyl ? "VINYL" : "DIGITAL STREAMER");
}

void readInitialPotState() {
    decca::pots::update();
    for (uint8_t i = 0; i < 4; ++i) {
        g_potValues[i] = decca::pots::value(kPots[i]);
    }
    g_viewState.volume = g_potValues[0];
    g_viewState.bass = g_potValues[1];
    g_viewState.treble = g_potValues[2];
    g_viewState.balance = g_potValues[3];
}

void updatePotState() {
    decca::pots::update();

    int8_t changedControl = -1;
    uint16_t* viewValues[4] = {
        &g_viewState.volume,
        &g_viewState.bass,
        &g_viewState.treble,
        &g_viewState.balance,
    };

    for (uint8_t i = 0; i < 4; ++i) {
        const uint16_t value = decca::pots::value(kPots[i]);
        const uint16_t change = value > g_potValues[i]
                                    ? value - g_potValues[i]
                                    : g_potValues[i] - value;
        if (change < kControlPresentationDeadband) {
            continue;
        }
        g_potValues[i] = value;
        *viewValues[i] = value;
        if (changedControl < 0) {
            changedControl = static_cast<int8_t>(i);
        }
    }

    if (changedControl >= 0 &&
        g_viewState.power == decca::display::PowerState::On) {
        decca::display::setState(g_viewState);
        const uint8_t index = static_cast<uint8_t>(changedControl);
        decca::display::showControl(kControls[index], g_potValues[index]);
    }
}

void applyPowerState() {
    const bool powerOn = decca::power::isOn();
    g_viewState.power = powerOn ? decca::display::PowerState::On
                                : decca::display::PowerState::Standby;
    decca::display::setState(g_viewState);

    Serial.print("[POWER] state=");
    Serial.println(powerOn ? "ON" : "STANDBY");
}

}  // namespace

void setup() {
    Serial.begin(115200);
    decca::hardware::init();
    decca::buttons::init();
    decca::pots::init();
    decca::power::init(
        decca::buttons::isPressed(decca::buttons::Button::OnOff));
    g_viewState.power = decca::power::isOn()
                            ? decca::display::PowerState::On
                            : decca::display::PowerState::Standby;
    readInitialPotState();
    decca::display::init();
    applySourceState(false);
    applyPowerState();
    decca::ota::init();
}

void loop() {
    decca::buttons::update();
    updatePotState();
    if (decca::power::update(
            decca::buttons::isPressed(decca::buttons::Button::OnOff))) {
        applyPowerState();
    }
    const decca::buttons::SourceMode sourceMode = decca::buttons::sourceMode();
    if (sourceMode != g_sourceMode) {
        applySourceState(true);
    }
    decca::display::update();
    decca::ota::update();
}
#endif

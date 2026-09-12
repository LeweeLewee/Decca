/** Phase 1 coordinator: logical power/display state plus continuous OTA. */
#include <Arduino.h>
#include <cstring>
#ifndef PIO_UNIT_TESTING
#include "buttons.h"
#include "display.h"
#include "hardware.h"
#include "lighting.h"
#include "ota.h"
#include "pots.h"
#include "power.h"
#include "settings.h"
#include "version.h"
#include "wiim.h"

namespace {

decca::display::ViewState g_viewState;
decca::buttons::SourceMode g_sourceMode =
    decca::buttons::SourceMode::DigitalStreamer;
uint16_t g_potValues[4]{};
constexpr uint16_t kControlPresentationDeadband = 5;
constexpr uint32_t kStreamerUnavailableRefreshMs = 1000;
decca::wiim::Status g_lastWiimStatus = decca::wiim::Status::Disabled;
uint32_t g_lastStreamerUnavailableRefreshMs = 0;
bool g_streamerUnavailablePresented = false;
decca::wiim::Playback g_lastPlayback = decca::wiim::Playback::None;
char g_lastTitle[decca::wiim::kTitleCapacity + 1]{};
char g_lastArtist[decca::wiim::kArtistCapacity + 1]{};
decca::settings::Source g_lastWiimDisplaySource =
    decca::settings::Source::DigitalStreamer;

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
    decca::wiim::requestSource(g_viewState.source);

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

    if (changedControl == 0) {
        decca::wiim::requestVolume(
            static_cast<uint8_t>((g_potValues[0] + 5U) / 10U));
    }
}

void applyPowerState() {
    const bool powerOn = decca::power::isOn();
    g_viewState.power = powerOn ? decca::display::PowerState::On
                                : decca::display::PowerState::Standby;
    decca::display::setState(g_viewState);
    decca::wiim::requestPower(powerOn);

    Serial.print("[POWER] state=");
    Serial.println(powerOn ? "ON" : "STANDBY");
}

void applyWiimState() {
    decca::wiim::update();
    const decca::wiim::Snapshot& snapshot = decca::wiim::snapshot();
    const bool statusChanged = snapshot.status != g_lastWiimStatus;
    const bool metadataChanged =
        snapshot.playback != g_lastPlayback ||
        std::strncmp(snapshot.title, g_lastTitle, sizeof(g_lastTitle)) != 0 ||
        std::strncmp(snapshot.artist, g_lastArtist, sizeof(g_lastArtist)) != 0 ||
        g_viewState.source != g_lastWiimDisplaySource;

    const bool streamerUnavailable =
        snapshot.status == decca::wiim::Status::Error &&
        g_viewState.power == decca::display::PowerState::On;
    if (streamerUnavailable) {
        const uint32_t now = millis();
        if (!g_streamerUnavailablePresented ||
            (now - g_lastStreamerUnavailableRefreshMs) >=
                kStreamerUnavailableRefreshMs) {
            decca::display::showStatus("STREAMER UNAVAILABLE");
            g_lastStreamerUnavailableRefreshMs = now;
            g_streamerUnavailablePresented = true;
        }
    } else {
        // Once communication recovers, stop extending the transient. The
        // display returns to its current dashboard without a forced redraw.
        g_streamerUnavailablePresented = false;
    }

    if (statusChanged) {
        g_lastWiimStatus = snapshot.status;
    }

    if (!metadataChanged) return;
    g_lastWiimDisplaySource = g_viewState.source;
    g_lastPlayback = snapshot.playback;
    std::strncpy(g_lastTitle, snapshot.title, sizeof(g_lastTitle) - 1U);
    std::strncpy(g_lastArtist, snapshot.artist, sizeof(g_lastArtist) - 1U);
    g_lastTitle[sizeof(g_lastTitle) - 1U] = '\0';
    g_lastArtist[sizeof(g_lastArtist) - 1U] = '\0';

    const bool digital =
        g_viewState.source == decca::settings::Source::DigitalStreamer;
    g_viewState.title = digital && snapshot.metadataValid ? g_lastTitle : nullptr;
    g_viewState.artist =
        digital && snapshot.metadataValid ? g_lastArtist : nullptr;
    g_viewState.playing = snapshot.playback == decca::wiim::Playback::Playing;
    decca::display::setState(g_viewState);
}

void applyLightingState() {
    const bool lightsRequested =
        decca::buttons::lightingRequest() ==
        decca::buttons::LightingRequest::On;
    const uint8_t target = decca::power::isOn() && lightsRequested
                               ? decca::settings::get().dial
                               : 0;
    if (decca::lighting::brightness(decca::lighting::Zone::Dial) == target) {
        return;
    }

    decca::lighting::setBrightness(decca::lighting::Zone::Dial, target);
    Serial.print("[LIGHTING] duty=");
    Serial.println(target);
}

}  // namespace

void setup() {
    // Establish lighting safe-off before serial, display or network setup.
    decca::hardware::init();
    Serial.begin(115200);
    Serial.print("[SYSTEM] firmware=");
    Serial.println(decca::version::kFirmwareVersion);
    decca::settings::init();
    decca::buttons::init();
    decca::pots::init();
    decca::lighting::init();
    decca::power::init(
        decca::buttons::isPressed(decca::buttons::Button::OnOff));
    applyLightingState();
    g_viewState.power = decca::power::isOn()
                            ? decca::display::PowerState::On
                            : decca::display::PowerState::Standby;
    readInitialPotState();
    decca::display::init();
    applySourceState(false);
    applyPowerState();
    decca::ota::init();
    decca::wiim::init();
    decca::wiim::requestSource(g_viewState.source);
    decca::wiim::requestVolume(
        static_cast<uint8_t>((g_potValues[0] + 5U) / 10U));
    decca::wiim::requestPower(decca::power::isOn());
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
    applyLightingState();
    applyWiimState();
    decca::display::update();
    decca::ota::update();
}
#endif

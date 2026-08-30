/** Phase 1 coordinator: logical power/display state plus continuous OTA. */
#include <Arduino.h>
#ifndef PIO_UNIT_TESTING
#include "buttons.h"
#include "display.h"
#include "hardware.h"
#include "ota.h"
#include "power.h"

namespace {

void applyPowerState() {
    const bool powerOn = decca::power::isOn();
    decca::display::ViewState state;
    state.power = powerOn ? decca::display::PowerState::On
                          : decca::display::PowerState::Standby;
    decca::display::setState(state);

    Serial.print("[POWER] state=");
    Serial.println(powerOn ? "ON" : "STANDBY");
}

}  // namespace

void setup() {
    Serial.begin(115200);
    decca::hardware::init();
    decca::buttons::init();
    decca::power::init(
        decca::buttons::isPressed(decca::buttons::Button::OnOff));
    decca::display::init();
    applyPowerState();
    decca::ota::init();
}

void loop() {
    decca::buttons::update();
    if (decca::power::update(
            decca::buttons::isPressed(decca::buttons::Button::OnOff))) {
        applyPowerState();
    }
    decca::display::update();
    decca::ota::update();
}
#endif

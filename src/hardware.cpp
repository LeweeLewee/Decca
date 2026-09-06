/**
 * @file    hardware.cpp
 * @brief   Board-level initialisation.
 */
#include "hardware.h"

#include <Arduino.h>
#include <Wire.h>

namespace decca::hardware {

void init() {
    // GPIO18 can float while the ESP32 resets. The external 10 kΩ pull-down
    // holds the DFR0457 input off before this code runs; take active control at
    // the first opportunity and keep it low until LEDC is attached at duty 0.
    pinMode(kDialLightingPwm, OUTPUT);
    digitalWrite(kDialLightingPwm, LOW);

    pinMode(kPotVolume, INPUT);
    pinMode(kPotBass, INPUT);
    pinMode(kPotTreble, INPUT);
    pinMode(kPotBalance, INPUT);

    analogReadResolution(kAdcResolutionBits);
    analogSetPinAttenuation(kPotVolume, ADC_11db);
    analogSetPinAttenuation(kPotBass, ADC_11db);
    analogSetPinAttenuation(kPotTreble, ADC_11db);
    analogSetPinAttenuation(kPotBalance, ADC_11db);

    pinMode(kSwitchOnOff, INPUT_PULLUP);
    pinMode(kButtonVhf, INPUT_PULLUP);
    pinMode(kSwitchStereoMono, INPUT_PULLUP);

    Wire.begin(kDisplaySda, kDisplayScl);

    ledcSetup(kDialLightingPwmChannel,
              kDialLightingPwmFrequencyHz,
              kDialLightingPwmResolutionBits);
    ledcAttachPin(kDialLightingPwm, kDialLightingPwmChannel);
    ledcWrite(kDialLightingPwmChannel, 0);
}

}  // namespace decca::hardware

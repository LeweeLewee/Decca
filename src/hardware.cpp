/**
 * @file    hardware.cpp
 * @brief   Board-level initialisation.
 */
#include "hardware.h"

#include <Arduino.h>
#include <Wire.h>

namespace decca::hardware {

void init() {
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

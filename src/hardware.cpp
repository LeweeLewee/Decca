/**
 * @file    hardware.cpp
 * @brief   Implementation of the board-level abstraction (see hardware.h).
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

    Wire.begin(kDisplaySda, kDisplayScl);

    // Establish the required safe boot state before lighting::init() owns fades.
    ledcSetup(kDialLightingPwmChannel,
              kDialLightingPwmFrequencyHz,
              kDialLightingPwmResolutionBits);
    ledcAttachPin(kDialLightingPwm, kDialLightingPwmChannel);
    ledcWrite(kDialLightingPwmChannel, 0);
}

}  // namespace decca::hardware

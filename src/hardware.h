/**
 * @file    hardware.h
 * @brief   Board-level pin map and hardware initialisation.
 */
#pragma once

#include <cstdint>

namespace decca::hardware {

// GPIO32–35, display GPIO21/22 and lighting PWM GPIO18 are verified.
// On/off GPIO14, VHF GPIO26 and Stereo/Mono GPIO25 are pending verification.
constexpr uint8_t kPotVolume = 32;
constexpr uint8_t kPotBass = 33;
constexpr uint8_t kPotTreble = 34;
constexpr uint8_t kPotBalance = 35;
constexpr uint8_t kSwitchOnOff = 14;
constexpr uint8_t kButtonVhf = 26;
constexpr uint8_t kSwitchStereoMono = 25;
constexpr uint8_t kDisplaySda = 21;
constexpr uint8_t kDisplayScl = 22;
constexpr uint8_t kDialLightingPwm = 18;

constexpr uint8_t kAdcResolutionBits = 12;
constexpr uint8_t kDialLightingPwmChannel = 0;
constexpr uint32_t kDialLightingPwmFrequencyHz = 1000;
constexpr uint8_t kDialLightingPwmResolutionBits = 8;

void init();

}  // namespace decca::hardware

/**
 * @file    hardware.h
 * @brief   Board-level pin map and hardware initialisation.
 */
#pragma once

#include <cstdint>

namespace decca::hardware {

// GPIO32–35, VHF GPIO23 and display GPIO21/22 are bench-verified.
// Stereo/Mono GPIO17 (TX2) is physically verified.
// On/off GPIO26 and lighting PWM GPIO18 await physical verification. Their
// previous GPIO19/GPIO25 assignments were physically verified.
constexpr uint8_t kPotVolume = 32;
constexpr uint8_t kPotBass = 33;
constexpr uint8_t kPotTreble = 34;
constexpr uint8_t kPotBalance = 35;
constexpr uint8_t kSwitchOnOff = 26;
constexpr uint8_t kButtonVhf = 23;
constexpr uint8_t kSwitchStereoMono = 17;
constexpr uint8_t kDisplaySda = 21;
constexpr uint8_t kDisplayScl = 22;
constexpr uint8_t kDialLightingPwm = 18;

constexpr uint8_t kAdcResolutionBits = 12;
constexpr uint8_t kDialLightingPwmChannel = 0;
constexpr uint32_t kDialLightingPwmFrequencyHz = 1000;
constexpr uint8_t kDialLightingPwmResolutionBits = 8;

void init();

}  // namespace decca::hardware

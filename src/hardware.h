/**
 * @file    hardware.h
 * @brief   Board-level pin map and hardware initialisation.
 */
#pragma once

#include <cstdint>

namespace decca::hardware {

// GPIO32–35, display GPIO21/22 and on/off GPIO19 are bench-verified.
// VHF GPIO26 and Stereo/Mono GPIO14 are proposed pending physical verification.
// Lighting PWM GPIO25 and the MOSFET/lamp load are physically verified.
constexpr uint8_t kPotVolume = 32;
constexpr uint8_t kPotBass = 33;
constexpr uint8_t kPotTreble = 34;
constexpr uint8_t kPotBalance = 35;
constexpr uint8_t kSwitchOnOff = 19;
constexpr uint8_t kButtonVhf = 26;
constexpr uint8_t kSwitchStereoMono = 14;
constexpr uint8_t kDisplaySda = 21;
constexpr uint8_t kDisplayScl = 22;
constexpr uint8_t kDialLightingPwm = 25;

constexpr uint8_t kAdcResolutionBits = 12;
constexpr uint8_t kDialLightingPwmChannel = 0;
constexpr uint32_t kDialLightingPwmFrequencyHz = 1000;
constexpr uint8_t kDialLightingPwmResolutionBits = 8;

void init();

}  // namespace decca::hardware

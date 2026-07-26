/**
 * @file    pots.cpp
 * @brief   Implementation of potentiometer input (see pots.h).
 */

#include "pots.h"

#include <Arduino.h>

#include "hardware.h"

namespace decca::pots {
namespace {

constexpr uint8_t kPotCount = 4;
constexpr uint8_t kSmoothingDivisor = 8;

constexpr uint8_t kPins[kPotCount] = {
    hardware::kPotVolume,
    hardware::kPotBass,
    hardware::kPotTreble,
    hardware::kPotBalance,
};

struct PotState {
    Calibration calibration{};
    uint16_t filteredRaw = 0;
    uint16_t normalised = 0;
    bool hasSample = false;
};

PotState g_states[kPotCount]{};
uint32_t g_lastSampleMs = 0;
bool g_hasSampledAll = false;

#ifdef PIO_UNIT_TESTING
testing::RawReader g_rawReader = nullptr;
#endif

bool indexFor(Pot pot, uint8_t& index) {
    const uint8_t candidate = static_cast<uint8_t>(pot);
    if (candidate >= kPotCount) {
        return false;
    }
    index = candidate;
    return true;
}

uint16_t readRaw(uint8_t pin) {
#ifdef PIO_UNIT_TESTING
    if (g_rawReader != nullptr) {
        return g_rawReader(pin);
    }
#endif
    const int reading = analogRead(pin);
    if (reading < 0) {
        return 0;
    }
    if (reading > kAdcRawMax) {
        return kAdcRawMax;
    }
    return static_cast<uint16_t>(reading);
}

uint16_t normalise(uint16_t raw, const Calibration& calibration) {
    const uint16_t clamped =
        raw < calibration.rawMin
            ? calibration.rawMin
            : (raw > calibration.rawMax ? calibration.rawMax : raw);
    const uint32_t span = calibration.rawMax - calibration.rawMin;
    const uint32_t offset = clamped - calibration.rawMin;
    uint16_t result = static_cast<uint16_t>(
        ((offset * kNormalisedMax) + (span / 2U)) / span);
    if (calibration.inverted) {
        result = kNormalisedMax - result;
    }
    return result;
}

void sample(PotState& state, uint8_t pin) {
    const uint16_t raw = readRaw(pin);
    const bool firstSample = !state.hasSample;

    if (firstSample) {
        state.filteredRaw = raw;
        state.hasSample = true;
    } else {
        const int32_t difference =
            static_cast<int32_t>(raw) - state.filteredRaw;
        int32_t step = difference / kSmoothingDivisor;
        if (step == 0 && difference != 0) {
            step = difference > 0 ? 1 : -1;
        }
        state.filteredRaw = static_cast<uint16_t>(
            static_cast<int32_t>(state.filteredRaw) + step);
    }

    const uint16_t candidate = normalise(state.filteredRaw, state.calibration);
    const uint16_t change =
        candidate > state.normalised ? candidate - state.normalised
                                     : state.normalised - candidate;
    if (firstSample || change >= state.calibration.deadband) {
        state.normalised = candidate;
    }
}

}  // namespace

void init() {
    for (auto& state : g_states) {
        state = PotState{};
    }
    g_lastSampleMs = 0;
    g_hasSampledAll = false;
}

void update() {
    const uint32_t now = millis();
    if (g_hasSampledAll && (now - g_lastSampleMs) < kSampleIntervalMs) {
        return;
    }

    for (uint8_t i = 0; i < kPotCount; ++i) {
        sample(g_states[i], kPins[i]);
    }
    g_lastSampleMs = now;
    g_hasSampledAll = true;
}

uint16_t value(Pot pot) {
    uint8_t index = 0;
    return indexFor(pot, index) ? g_states[index].normalised : kNormalisedMin;
}

uint16_t rawValue(Pot pot) {
    uint8_t index = 0;
    return indexFor(pot, index) ? g_states[index].filteredRaw : 0;
}

bool setCalibration(Pot pot, const Calibration& calibration) {
    uint8_t index = 0;
    if (!indexFor(pot, index) || calibration.rawMin >= calibration.rawMax ||
        calibration.rawMax > kAdcRawMax ||
        calibration.deadband > kNormalisedMax) {
        return false;
    }

    g_states[index].calibration = calibration;
    g_states[index].filteredRaw = 0;
    g_states[index].normalised = 0;
    g_states[index].hasSample = false;
    g_hasSampledAll = false;
    return true;
}

Calibration calibration(Pot pot) {
    uint8_t index = 0;
    return indexFor(pot, index) ? g_states[index].calibration : Calibration{};
}

#ifdef PIO_UNIT_TESTING
namespace testing {

void setRawReader(RawReader reader) {
    g_rawReader = reader;
}

void resetRawReader() {
    g_rawReader = nullptr;
}

}  // namespace testing
#endif

}  // namespace decca::pots

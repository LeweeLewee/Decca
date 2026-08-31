/**
 * @file    settings.h
 * @brief   Persisted configuration and shared runtime state.
 */
#pragma once

#include <cstdint>

namespace decca::settings {

/** Owner-approved normal dial-lighting level: 90% of 8-bit PWM. */
constexpr uint8_t kDefaultDialBrightness = 230;

enum class Source : uint8_t {
    DigitalStreamer,
    Vinyl,
};

struct State {
    Source source = Source::DigitalStreamer;
    uint8_t volume = 0;
    uint8_t dial = kDefaultDialBrightness;
};

void init();
const State& get();
void set(const State& state);
void save();

}  // namespace decca::settings

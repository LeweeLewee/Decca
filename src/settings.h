/**
 * @file    settings.h
 * @brief   Persisted configuration and shared runtime state.
 */
#pragma once

#include <cstdint>

namespace decca::settings {

enum class Source : uint8_t {
    DigitalStreamer,
    Vinyl,
};

struct State {
    Source source = Source::DigitalStreamer;
    uint8_t volume = 0;
    uint8_t dial = 0;
};

void init();
const State& get();
void set(const State& state);
void save();

}  // namespace decca::settings

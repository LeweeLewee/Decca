/**
 * @file    settings.h
 * @brief   Persisted configuration and shared runtime state.
 *
 * settings is the one place modules exchange durable state. It holds user
 * preferences and the current device state, persists them to non-volatile
 * storage (NVS), and reloads them at boot. Because it is the shared data hub,
 * settings deliberately depends on no other module — the coupling points one
 * way only, keeping the input/output modules independent of each other.
 *
 * Responsibility:  own configuration/state; load and save to NVS.
 * Depends on:      nothing (other modules depend on it).
 * Used by:         most modules (read); a few (write) via the accessors here.
 */

#pragma once

#include <cstdint>

namespace decca::settings {

/**
 * @brief Input source selection.
 */
enum class Source {
    Vhf,
    Mw,
    Lw,
    Gram,
};

/**
 * @brief Persisted / shared state.
 *
 * Kept as a small plain struct so any module can read a coherent snapshot.
 */
struct State {
    Source source = Source::Vhf;
    uint8_t volume = 0;  // 0–255
    uint8_t dial = 0;    // dial brightness 0–255
};

/**
 * @brief Load persisted settings from NVS (or defaults on first boot).
 */
void init();

/**
 * @brief Read-only access to the current state snapshot.
 */
const State& get();

/**
 * @brief Replace the current state and mark it dirty for persistence.
 */
void set(const State& state);

/**
 * @brief Flush dirty state to NVS if anything changed. Non-blocking-friendly;
 *        call periodically rather than on every field change.
 */
void save();

}  // namespace decca::settings

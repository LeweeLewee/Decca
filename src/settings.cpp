/**
 * @file    settings.cpp
 * @brief   Implementation of persisted configuration/state (see settings.h).
 */

#include "settings.h"

#include <Preferences.h>

namespace decca::settings {

namespace {

#ifdef PIO_UNIT_TESTING
constexpr char kNamespace[] = "decca-test";
#else
constexpr char kNamespace[] = "decca";
#endif

constexpr char kStateKey[] = "state";
constexpr uint8_t kCurrentVersion = 1;

struct PersistedState {
    uint8_t version;
    uint8_t source;
    uint8_t volume;
    uint8_t dial;
};

static_assert(sizeof(PersistedState) == 4,
              "Persisted settings layout must remain fixed-width");

State g_state;
bool g_dirty = false;

bool isValid(const PersistedState& persisted) {
    return persisted.version == kCurrentVersion &&
           persisted.source <= static_cast<uint8_t>(Source::Gram);
}

State fromPersisted(const PersistedState& persisted) {
    State state;
    state.source = static_cast<Source>(persisted.source);
    state.volume = persisted.volume;
    state.dial = persisted.dial;
    return state;
}

PersistedState toPersisted(const State& state) {
    return {
        kCurrentVersion,
        static_cast<uint8_t>(state.source),
        state.volume,
        state.dial,
    };
}

bool statesEqual(const State& lhs, const State& rhs) {
    return lhs.source == rhs.source && lhs.volume == rhs.volume &&
           lhs.dial == rhs.dial;
}

}  // namespace

void init() {
    g_state = State{};
    g_dirty = false;

    Preferences preferences;
    if (!preferences.begin(kNamespace, true)) {
        return;
    }

    PersistedState persisted{};
    if (preferences.getBytesLength(kStateKey) == sizeof(persisted) &&
        preferences.getBytes(kStateKey, &persisted, sizeof(persisted)) ==
            sizeof(persisted) &&
        isValid(persisted)) {
        g_state = fromPersisted(persisted);
    }

    preferences.end();
}

const State& get() {
    return g_state;
}

void set(const State& state) {
    if (statesEqual(g_state, state)) {
        return;
    }

    g_state = state;
    g_dirty = true;
}

void save() {
    if (!g_dirty) {
        return;
    }

    Preferences preferences;
    if (!preferences.begin(kNamespace, false)) {
        return;
    }

    const PersistedState persisted = toPersisted(g_state);
    const bool saved =
        preferences.putBytes(kStateKey, &persisted, sizeof(persisted)) ==
        sizeof(persisted);
    preferences.end();

    if (saved) {
        g_dirty = false;
    }
}

}  // namespace decca::settings

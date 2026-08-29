/**
 * @file    settings.cpp
 * @brief   Persisted configuration and shared runtime state.
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
constexpr uint8_t kCurrentVersion = 2;

struct PersistedState {
    uint8_t version;
    uint8_t volume;
    uint8_t dial;
};

static_assert(sizeof(PersistedState) == 3,
              "Persisted settings layout must remain fixed-width");

State g_state;
bool g_dirty = false;

bool isValid(const PersistedState& persisted) {
    return persisted.version == kCurrentVersion;
}

PersistedState toPersisted(const State& state) {
    return {kCurrentVersion, state.volume, state.dial};
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
        g_state.volume = persisted.volume;
        g_state.dial = persisted.dial;
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

/**
 * @file wiim.h
 * @brief Non-blocking WiiM Pro local-HTTPS control and status interface.
 */
#pragma once

#include <cstddef>
#include <cstdint>

#include "settings.h"

namespace decca::wiim {

constexpr uint32_t kPlayerPollIntervalMs = 1000;
constexpr uint32_t kMetadataPollIntervalMs = 2000;
constexpr uint16_t kRequestTimeoutMs = 750;
constexpr uint8_t kTitleCapacity = 32;
constexpr uint8_t kArtistCapacity = 24;

enum class Status : uint8_t {
    Disabled,
    WaitingForNetwork,
    Connecting,
    Ready,
    Error,
};

enum class Playback : uint8_t {
    None,
    Stopped,
    Playing,
    Paused,
    Loading,
};

struct Snapshot {
    Status status = Status::Disabled;
    Playback playback = Playback::None;
    int16_t mode = -1;
    uint8_t volume = 0;
    bool muted = false;
    bool metadataValid = false;
    char title[kTitleCapacity + 1]{};
    char artist[kArtistCapacity + 1]{};
};

/** Start the worker task when Wi-Fi and a local WiiM host are configured. */
void init();

/** Copy worker state into the coordinator-facing snapshot; never blocks. */
void update();

/** Request the source implied by the physical VHF selector. */
void requestSource(settings::Source source);

/** Request WiiM output volume, clamped to 0-100. */
void requestVolume(uint8_t volume);

/** Request user-visible on/standby behaviour without removing WiiM power. */
void requestPower(bool on);

bool configured();
const Snapshot& snapshot();

#ifdef PIO_UNIT_TESTING
namespace testing {
void reset();
bool parsePlayerStatus(const char* json, Snapshot& output);
bool parseMetadata(const char* json, Snapshot& output);
const char* sourceCommand(settings::Source source);
}
#endif

}  // namespace decca::wiim

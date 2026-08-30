/**
 * @file    buttons.h
 * @brief   Debounced retained on/off, VHF and Stereo/Mono contacts.
 *
 * The original selector PCB is unreliable for multi-button electrical use.
 * Only the reliable VHF contact is read. Its stable state is authoritative:
 * latched/closed selects Digital Streamer; released/open selects Vinyl.
 * The Stereo/Mono contact closes in Mono: open Stereo requests dial lights on;
 * closed Mono requests them off. The lighting output is commissioned separately.
 */
#pragma once

#include <cstdint>

namespace decca::buttons {

enum class Button : uint8_t {
    None,
    OnOff,
    Vhf,
    StereoMono,
};

enum class SourceMode : uint8_t {
    DigitalStreamer,
    Vinyl,
};

enum class LightingRequest : uint8_t {
    Off,
    On,
};

constexpr uint32_t kDebounceMs = 25;

void init();
void update();
Button nextEvent();
bool isPressed(Button button);

/**
 * @return DigitalStreamer while the debounced VHF contact is closed;
 *         otherwise Vinyl. Call after update() in the main loop.
 */
SourceMode sourceMode();

/**
 * @return On while the contact is open in Stereo; Off while closed in Mono.
 */
LightingRequest lightingRequest();

#ifdef PIO_UNIT_TESTING
namespace testing {
using RawReader = int (*)(uint8_t pin);
void setRawReader(RawReader reader);
void resetRawReader();
}  // namespace testing
#endif

}  // namespace decca::buttons

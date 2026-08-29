/**
 * @file    buttons.h
 * @brief   Debounced retained on/off switch and sole Gram source contact.
 *
 * The original selector PCB is unreliable for multi-button electrical use.
 * Only the verified Gram contact is read. Its stable state is authoritative:
 * latched/closed selects Vinyl; released/open selects Digital Streamer.
 */
#pragma once

#include <cstdint>

namespace decca::buttons {

enum class Button : uint8_t {
    None,
    OnOff,
    Gram,
};

enum class SourceMode : uint8_t {
    DigitalStreamer,
    Vinyl,
};

constexpr uint32_t kDebounceMs = 25;

void init();
void update();
Button nextEvent();
bool isPressed(Button button);

/**
 * @return Vinyl while the debounced Gram contact is closed; otherwise
 *         DigitalStreamer. Call after update() in the main loop.
 */
SourceMode sourceMode();

#ifdef PIO_UNIT_TESTING
namespace testing {
using RawReader = int (*)(uint8_t pin);
void setRawReader(RawReader reader);
void resetRawReader();
}  // namespace testing
#endif

}  // namespace decca::buttons

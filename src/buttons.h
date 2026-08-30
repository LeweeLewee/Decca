/**
 * @file    buttons.h
 * @brief   Debounced retained on/off switch and sole VHF source contact.
 *
 * The original selector PCB is unreliable for multi-button electrical use.
 * Only the reliable VHF contact is read. Its stable state is authoritative:
 * latched/closed selects Digital Streamer; released/open selects Vinyl.
 */
#pragma once

#include <cstdint>

namespace decca::buttons {

enum class Button : uint8_t {
    None,
    OnOff,
    Vhf,
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
 * @return DigitalStreamer while the debounced VHF contact is closed;
 *         otherwise Vinyl. Call after update() in the main loop.
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

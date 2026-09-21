#pragma once
#include <cstdint>

namespace decca::health {
// Pure bounded aggregation: caller owns synchronisation.
struct Window {
    bool hasRssi = false;
    int32_t minRssi = 0;
    uint32_t maxLoopGapUs = 0;
    uint32_t samples = 0;
};
struct Counters {
    uint32_t wifiDisconnects = 0;
    uint32_t wiimFaults = 0;
};
class Aggregator {
 public:
    void wifi(bool connected) {
        if (wifiSeen_ && wifiConnected_ && !connected) ++counters.wifiDisconnects;
        wifiSeen_ = true;
        wifiConnected_ = connected;
    }
    void wiim(bool fault) {
        if (fault && !wiimFault_) ++counters.wiimFaults;
        wiimFault_ = fault;
    }
    void sample(bool connected, int32_t rssi) {
        ++window.samples;
        if (connected && (!window.hasRssi || rssi < window.minRssi)) {
            window.hasRssi = true;
            window.minRssi = rssi;
        }
    }
    void loopGap(uint32_t us) {
        if (us > window.maxLoopGapUs) window.maxLoopGapUs = us;
    }
    Window take() {
        const Window result = window;
        window = Window{};
        return result;
    }
    void restore(const Window& failed) {
        if (failed.hasRssi && (!window.hasRssi || failed.minRssi < window.minRssi)) {
            window.hasRssi = true;
            window.minRssi = failed.minRssi;
        }
        if (failed.maxLoopGapUs > window.maxLoopGapUs)
            window.maxLoopGapUs = failed.maxLoopGapUs;
        window.samples += failed.samples;
    }
    Counters counters;
    Window window;
 private:
    bool wifiSeen_ = false;
    bool wifiConnected_ = false;
    bool wiimFault_ = false;
};
inline bool due(uint32_t now, uint32_t previous, uint32_t interval) {
    return static_cast<uint32_t>(now - previous) >= interval;
}
}  // namespace decca::health

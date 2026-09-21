#include "../../src/health_model.h"
#include <cassert>
#include <cstdint>
#include <iostream>
using namespace decca::health;
int main() {
    Aggregator a;
    a.wifi(false);
    assert(a.counters.wifiDisconnects == 0); // initial offline is not a drop
    a.wifi(true); a.wifi(false); a.wifi(false); a.wifi(true); a.wifi(false);
    assert(a.counters.wifiDisconnects == 2);
    a.wiim(true); a.wiim(true); a.wiim(false); a.wiim(true);
    assert(a.counters.wiimFaults == 2);
    a.sample(false, 0);
    assert(!a.window.hasRssi);
    a.sample(true, -48); a.sample(true, -81); a.sample(true, -55);
    a.loopGap(12); a.loopGap(50001); a.loopGap(100);
    Window first = a.take();
    assert(first.hasRssi && first.minRssi == -81 && first.samples == 4);
    assert(first.maxLoopGapUs == 50001);
    assert(a.window.samples == 0 && !a.window.hasRssi);
    // New samples arriving during failed publish must survive restoration.
    a.sample(true, -90); a.loopGap(60000);
    a.restore(first);
    assert(a.window.minRssi == -90 && a.window.samples == 5);
    assert(a.window.maxLoopGapUs == 60000);
    assert(a.counters.wifiDisconnects == 2 && a.counters.wiimFaults == 2);
    a.take();
    a.restore(first);
    assert(a.window.minRssi == -81 && a.window.samples == 4);
    assert(!due(299999, 0, 300000));
    assert(due(300000, 0, 300000));
    assert(due(100, UINT32_MAX - 299899, 300000));
    assert(!due(100, UINT32_MAX - 9, 300000));
    std::cout << "health aggregation, failed-send recovery and timer wrap: PASS\n";
}

#pragma once
#include <cstdint>
#ifndef DECCA_HEALTH_ENABLED
#define DECCA_HEALTH_ENABLED 0
#endif

namespace decca::health {
/** Read-only values supplied by main. No calls to other firmware modules. */
struct Inputs {
    bool powerOn = false;
    bool vinyl = false;
    bool wiimFault = false;
    // Stable strings supplied by main; copied into fixed-size storage.
    const char* wiimStatus = "disabled";
};
/** Optional trial only. Missing broker config leaves the feature disabled.
 * Network work runs outside the coordinator. No NVS or GPIO writes.
 */
void init();
/** Fixed-size state copy, Wi-Fi sampling at 1 Hz, loop-gap aggregation.
 * No MQTT calls, socket work, allocation or waits in this function.
 */
void update(const Inputs& inputs);
}  // namespace decca::health

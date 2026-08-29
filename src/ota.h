#pragma once
#include <cstdint>
namespace decca::ota {
enum class Status : uint8_t { Disabled, Connecting, Ready, Updating, Error };
constexpr uint32_t kReconnectIntervalMs = 10000;
void init();
void update();
bool configured();
bool ready();
Status status();
#ifdef PIO_UNIT_TESTING
namespace testing {
using TimeProvider = uint32_t (*)();
using ConnectedProvider = bool (*)();
using Action = void (*)();
void setConfigured(bool value);
void setTimeProvider(TimeProvider provider);
void setConnectedProvider(ConnectedProvider provider);
void setConnectAction(Action action);
void setServiceActions(Action begin, Action handle, Action end);
void resetHooks();
}
#endif
}

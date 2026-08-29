#include "unity_runner.h"
#include "ota.h"
using decca::ota::Status;
namespace {
uint32_t nowMs=0;bool connected=false;uint8_t connects=0,begins=0,handles=0,ends=0;
uint32_t timeFn(){return nowMs;} bool connectedFn(){return connected;}
void connectFn(){++connects;} void beginFn(){++begins;} void handleFn(){++handles;} void endFn(){++ends;}
void reset(bool configured){nowMs=0;connected=false;connects=begins=handles=ends=0;decca::ota::testing::resetHooks();decca::ota::testing::setConfigured(configured);decca::ota::testing::setTimeProvider(timeFn);decca::ota::testing::setConnectedProvider(connectedFn);decca::ota::testing::setConnectAction(connectFn);decca::ota::testing::setServiceActions(beginFn,handleFn,endFn);}
}
void test_disabled(){reset(false);decca::ota::init();TEST_ASSERT_FALSE(decca::ota::configured());TEST_ASSERT_EQUAL((int)Status::Disabled,(int)decca::ota::status());TEST_ASSERT_EQUAL_UINT8(0,connects);}
void test_nonblocking_connect(){reset(true);decca::ota::init();TEST_ASSERT_EQUAL((int)Status::Connecting,(int)decca::ota::status());TEST_ASSERT_EQUAL_UINT8(1,connects);TEST_ASSERT_EQUAL_UINT8(0,begins);}
void test_retry_interval(){reset(true);decca::ota::init();nowMs=decca::ota::kReconnectIntervalMs-1;decca::ota::update();TEST_ASSERT_EQUAL_UINT8(1,connects);++nowMs;decca::ota::update();TEST_ASSERT_EQUAL_UINT8(2,connects);}
void test_service_once(){reset(true);decca::ota::init();connected=true;decca::ota::update();decca::ota::update();TEST_ASSERT_TRUE(decca::ota::ready());TEST_ASSERT_EQUAL_UINT8(1,begins);TEST_ASSERT_EQUAL_UINT8(2,handles);}
void test_wifi_loss(){reset(true);decca::ota::init();connected=true;decca::ota::update();connected=false;decca::ota::update();TEST_ASSERT_EQUAL((int)Status::Connecting,(int)decca::ota::status());TEST_ASSERT_EQUAL_UINT8(1,ends);}
void runAll(){RUN_TEST(test_disabled);RUN_TEST(test_nonblocking_connect);RUN_TEST(test_retry_interval);RUN_TEST(test_service_once);RUN_TEST(test_wifi_loss);}

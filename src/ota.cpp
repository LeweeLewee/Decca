#include "ota.h"
#include <Arduino.h>
#include <ArduinoOTA.h>
#include <WiFi.h>
#if __has_include("secrets.h")
#include "secrets.h"
#endif
#ifndef DECCA_WIFI_SSID
#define DECCA_WIFI_SSID ""
#endif
#ifndef DECCA_WIFI_PASSWORD
#define DECCA_WIFI_PASSWORD ""
#endif
#ifndef DECCA_OTA_PASSWORD
#define DECCA_OTA_PASSWORD ""
#endif
namespace decca::ota {
namespace {
constexpr char kHostname[]="decca";
Status g_status=Status::Disabled;
bool g_serviceStarted=false;
uint32_t g_lastConnectAttemptMs=0;
#ifdef PIO_UNIT_TESTING
int8_t g_testConfigured=-1;
testing::TimeProvider g_timeProvider=nullptr;
testing::ConnectedProvider g_connectedProvider=nullptr;
testing::Action g_connectAction=nullptr;
testing::Action g_beginAction=nullptr;
testing::Action g_handleAction=nullptr;
testing::Action g_endAction=nullptr;
#endif
bool hasText(const char* value){return value!=nullptr&&value[0]!='\0';}
uint32_t nowMs(){
#ifdef PIO_UNIT_TESTING
 if(g_timeProvider)return g_timeProvider();
#endif
 return millis();
}
bool hasConfiguration(){
#ifdef PIO_UNIT_TESTING
 if(g_testConfigured>=0)return g_testConfigured==1;
#endif
 return hasText(DECCA_WIFI_SSID)&&hasText(DECCA_OTA_PASSWORD);
}
bool networkConnected(){
#ifdef PIO_UNIT_TESTING
 if(g_connectedProvider)return g_connectedProvider();
#endif
 return WiFi.status()==WL_CONNECTED;
}
void startConnection(){
#ifdef PIO_UNIT_TESTING
 if(g_connectAction){g_connectAction();return;}
#endif
 WiFi.mode(WIFI_STA); WiFi.persistent(false); WiFi.setAutoReconnect(true);
 WiFi.setHostname(kHostname); WiFi.begin(DECCA_WIFI_SSID,DECCA_WIFI_PASSWORD);
 Serial.println("[OTA] connecting to Wi-Fi");
}
void beginService(){
#ifdef PIO_UNIT_TESTING
 if(g_beginAction){g_beginAction();return;}
#endif
 ArduinoOTA.begin();
}
void handleService(){
#ifdef PIO_UNIT_TESTING
 if(g_handleAction){g_handleAction();return;}
#endif
 ArduinoOTA.handle();
}
void endService(){
#ifdef PIO_UNIT_TESTING
 if(g_endAction){g_endAction();return;}
#endif
 ArduinoOTA.end();
}
void configureService(){
 ArduinoOTA.setHostname(kHostname);
 ArduinoOTA.setPassword(DECCA_OTA_PASSWORD);
 ArduinoOTA.onStart([](){g_status=Status::Updating;Serial.println("[OTA] update started");});
 ArduinoOTA.onEnd([](){g_status=Status::Ready;Serial.println("[OTA] update complete; rebooting");});
 ArduinoOTA.onError([](ota_error_t error){g_status=Status::Error;Serial.printf("[OTA] error %u\n",static_cast<unsigned>(error));});
}
}
void init(){
 g_serviceStarted=false;
 if(!hasConfiguration()){g_status=Status::Disabled;Serial.println("[OTA] disabled: create src/secrets.h");return;}
 configureService(); g_status=Status::Connecting;
 g_lastConnectAttemptMs=nowMs(); startConnection();
}
void update(){
 if(g_status==Status::Disabled)return;
 if(networkConnected()){
  if(!g_serviceStarted){beginService();g_serviceStarted=true;g_status=Status::Ready;Serial.print("[OTA] ready at ");Serial.print(WiFi.localIP());Serial.println(" (decca.local)");}
  handleService();return;
 }
 if(g_serviceStarted){endService();g_serviceStarted=false;}
 g_status=Status::Connecting;
 const uint32_t now=nowMs();
 if((now-g_lastConnectAttemptMs)>=kReconnectIntervalMs){g_lastConnectAttemptMs=now;startConnection();}
}
bool configured(){return hasConfiguration();}
bool ready(){return g_status==Status::Ready;}
Status status(){return g_status;}
#ifdef PIO_UNIT_TESTING
namespace testing {
void setConfigured(bool value){g_testConfigured=value?1:0;}
void setTimeProvider(TimeProvider p){g_timeProvider=p;}
void setConnectedProvider(ConnectedProvider p){g_connectedProvider=p;}
void setConnectAction(Action a){g_connectAction=a;}
void setServiceActions(Action b,Action h,Action e){g_beginAction=b;g_handleAction=h;g_endAction=e;}
void resetHooks(){g_testConfigured=-1;g_timeProvider=nullptr;g_connectedProvider=nullptr;g_connectAction=nullptr;g_beginAction=nullptr;g_handleAction=nullptr;g_endAction=nullptr;}
}
#endif
}

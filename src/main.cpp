/** Safe bootstrap runtime: safe pins plus continuous OTA servicing. */
#include <Arduino.h>
#ifndef PIO_UNIT_TESTING
#include "hardware.h"
#include "ota.h"
void setup(){Serial.begin(115200);decca::hardware::init();decca::ota::init();}
void loop(){decca::ota::update();}
#endif

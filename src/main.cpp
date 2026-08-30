/** Safe bootstrap runtime: safe pins plus continuous OTA servicing. */
#include <Arduino.h>
#ifndef PIO_UNIT_TESTING
#include "display.h"
#include "hardware.h"
#include "ota.h"
void setup(){
    Serial.begin(115200);
    decca::hardware::init();
    decca::display::init();
    decca::display::showCalibrationPattern();
    decca::ota::init();
}
void loop(){
    decca::display::update();
    decca::ota::update();
}
#endif

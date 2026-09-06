#pragma once

#ifdef DECCA_ADC_DIAGNOSTIC

namespace decca::adc_diagnostic {

void init();
void update();
bool ownsLighting();

}  // namespace decca::adc_diagnostic

#endif

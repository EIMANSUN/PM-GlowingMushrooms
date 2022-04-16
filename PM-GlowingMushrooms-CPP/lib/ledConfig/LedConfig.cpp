#include <Arduino.h>
#include "LedConfig.h"

LedConfig::LedConfig(int *min, int period) { //short min[3], short max[3], 

    this->_period = period;
    //_max[3] = max[3];
}

int LedConfig::getPeriod() {
    return _period;
}

void LedConfig::displayArray() {
    
}
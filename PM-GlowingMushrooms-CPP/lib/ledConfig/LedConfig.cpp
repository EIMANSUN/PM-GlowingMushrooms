#include <Arduino.h>
#include "LedConfig.h"

LedConfig::LedConfig(int period) {

    _period = period;
}

int LedConfig::getPeriod() {
    return this->_period;
}
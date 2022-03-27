/*
    LedConfig.h Is an object of RGB led configuration for dynamic change in color
    Created by Eimantas Vengris March 27, 2022
*/

#ifndef LedConfig_h
#define LedConfig_h

#include <Arduino.h>

class LedConfig {
    public:
        LedConfig(int period);
        int getPeriod();



    private:
        int _period;
};

#endif
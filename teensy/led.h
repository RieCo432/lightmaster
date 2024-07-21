#include <FastLED.h>
#include <tuple>
#include "config.h"

#ifndef LED_H
#define LED_H

class Led {
  public:
    float pos_x;
    float pos_y;
    float pos_z;

    float apparent_pos_x;
    float apparent_pos_y;
    float apparent_pos_z;

    float offset_x = 0;
    float offset_y = 0;
    float offset_z = 0;

    float apparent_angle_alpha;
    float apparent_angle_beta;

    RainbowEffect* activeRainbowEffect = NULL;

    Led();
    Led(float x, float y, float z);
    void getPositionString(char* buffer);
    void getApparentPositionString(char* buffer);
    void getApparentAnglesString(char* buffer);
    void setOffsets(float x, float y, float z);
    std::tuple<float, float> setApparentAngles();
    void closeApparentAngles(float factor_alpha, float factor_beta);
    
    CRGB getColour(uint32_t time_elapsed);
};
#endif
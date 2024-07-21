#include <FastLED.h>

#ifndef LED_H
#define LED_H

class Led {
  public:
    float pos_x;
    float pos_y;
    float pos_z;

    float offset_x = 0;
    float offset_y = 0;
    float offset_z = 0;

    float apparent_angle_horizontal;
    float apparent_angle_vertical;

    CRGB* colour;

    Led();
    Led(float x, float y, float z);
    void getPositionString(char* buffer);
    void getApparentPositionString(char* buffer);
    void setOffsets(float x, float y, float z);
    void setApparentAngles();
};
#endif
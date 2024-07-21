#ifndef ELEMENT_H
#define ELEMENT_H
#include "led.h"

class Element {
  public:
    float from_pos_x;
    float from_pos_y;
    float from_pos_z;

    float to_pos_x;
    float to_pos_y;
    float to_pos_z;

    int num_leds;

    Led *start_led;
    Led *next_led;

    Element();
    Element(float from_x, float from_y, float from_z, float to_x, float to_y, float to_z, int length, Led* first_led);
    
    void setLedOffsets(float offset_x, float offset_y, float offset_z);
    void setLedApparentAngles();

};

#endif
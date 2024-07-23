#ifndef ELEMENT_H
#define ELEMENT_H
#include "led.h"
#include <tuple>
#include "config.h"
#include <FastLED.h>

class Element {
  public:
    float from_pos_x;
    float from_pos_y;
    float from_pos_z;

    float to_pos_x;
    float to_pos_y;
    float to_pos_z;

    int num_leds;

    CRGB *strip_start;

    Led *start_led;
    Led *next_led;

    Effect effect = {.enabled = false, .brightness = 1.0, .name = "rainbow"};
    RainbowEffect rainbowEffect = {.period = 0, .hue_start = 0, .hue_end = 360, .direction = 0, .compress = 1};

    Element();
    Element(float from_x, float from_y, float from_z, float to_x, float to_y, float to_z, int length, Led* first_led, CRGB* strip);
    
    void setLedOffsets(float offset_x, float offset_y, float offset_z);
    std::tuple<float, float, float, float> setLedApparentAngles();
    void closeLedApparentAngles(float factor_alpha, float factor_beta);
    void setRainbowEffect(RainbowEffect* newRainbowEffect);
    void setStripColours();
};

#endif
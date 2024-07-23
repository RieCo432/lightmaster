#ifndef ELEMENT_H
#define ELEMENT_H
#include "led.h"
#include <tuple>
#include "config.h"
#include <FastLED.h>
#include <Arduino.h>

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

    int bar_1_max_index = 0;
    int bar_2_max_index = 0;

    int bar_1_peak_index = 0;
    int bar_2_peak_index = 0;


    Effect effect = {
      .enabled = false,
      .name = "audio"
    };

    RainbowEffect rainbowEffect = {
      .period = 0,
      .hue_start = 0,
      .hue_end = 360,
      .direction = 0,
      .compress = 1,
      .value = 1.0,
      .saturation = 1.0
    };

    AudioEffect audioEffect = {
      .show_peaks = true,
      .hue_offset_low = 0,
      .hue_offset_high = 120,
      .hue_offset_peak = 240,
      .hue_start = 0,
      .hue_end = 1,
      .period = 0,
      .value = 1.0,
      .saturation = 1.0,
      
      .absolute_range = false,
      .range_to_max = 0.5,
      .reverse = true,

      .dual_bars = false,
  
      .middle_out = false,

      .bar_1_bin_start = 0,
      .bar_1_bin_end = 10,

      .bar_2_bin_start = 10,
      .bar_2_bin_end = 20,

    };

    Element();
    Element(float from_x, float from_y, float from_z, float to_x, float to_y, float to_z, int length, Led* first_led, CRGB* strip);
    
    void setLedOffsets(float offset_x, float offset_y, float offset_z);
    std::tuple<float, float, float, float> setLedApparentAngles();
    void closeLedApparentAngles(float factor_alpha, float factor_beta);
    void setRainbowEffect(RainbowEffect* newRainbowEffect);
    void setStripColours();
    void runRainbow();
    void runAudio();
};

#endif
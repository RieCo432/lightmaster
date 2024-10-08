#ifndef ELEMENT_H
#define ELEMENT_H
#include "led.h"
#include <tuple>
#include "config.h"
#include <FastLED.h>
#include <Arduino.h>
#include <ArduinoJson.h>

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

    float *audio_bins;

    int bar_1_max_index = 0;
    int bar_2_max_index = 0;

    float bar_1_peak_proto_index = 5.0;
    float bar_2_peak_proto_index = 5.0;

    int bar_1_peak_index;
    int bar_2_peak_index;

    bool *audio_mask;


    Effect effect = {
      .enabled = true,
      .name = "dual_zone"
    };

    RainbowEffect rainbowEffect = {
      .period = 20,
      .hue_start = 0,
      .hue_end = 360,
      .direction = 0,
      .compress = 4,
      .value = 1.0,
      .saturation = 1.0
    };

    AudioEffect audioEffect = {
      .baseEffect = "rainbow",
      .show_peaks = true,

      .max_fallback_divider = 1.3,
      .peak_fallback_rate = 1.0
    };

    SpectrumBars spectrumBars = {
      .hue_offset_low = 0,
      .hue_offset_high = 120,
      .hue_offset_peak = 240,
      .hue_start = 0,
      .hue_end = 180,
      .period = 5,
      .value = 1.0,
      .saturation = 1.0,
      
      .absolute_range = true,
      .range_to_max = 30,
    };

    AudioBins audioBins {
      .reverse = false,

      .dual_bars = true,
  
      .middle_out = false,

      .bar_1_bin_start = 0,
      .bar_1_bin_end = 255,

      .bar_2_bin_start = 256,
      .bar_2_bin_end = 511,
    };

    Element();
    Element(float from_x, float from_y, float from_z, float to_x, float to_y, float to_z, int length, Led* first_led, CRGB* strip, float* fft_audio_bins);
    
    void setLedOffsets(float offset_x, float offset_y, float offset_z);
    void setLedViewer(float viewer_x, float viewer_y, float viewer_z);
    std::tuple<float, float, float, float> setLedApparentAngles();
    void closeLedApparentAngles(float factor_alpha, float factor_beta);
    void setEffect(JsonDocument config);
    void setAudioEffect(JsonDocument config);
    void setRainbowEffect(JsonDocument config);
    void setAudioBins(JsonDocument config);
    void setSpectrumBars(JsonDocument config);
    void setStripColours();
    void applyRainbowBackground();
    void applySpectrumBarsBackground();
    void calculateAudioMask();
    void applyAudioMask();
    void applyDualZone();
};

#endif
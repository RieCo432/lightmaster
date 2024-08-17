#ifndef CONFIG_H
#define CONFIG_H


typedef struct {
  bool enabled;
  char name[24];
} Effect;


typedef struct {
  float period;
  float hue_start;
  float hue_end;
  int direction;  // 0 = horizontal, 1 = vertical
  int compress; // how many times is the pattern repeated
  float value;
  float saturation;
} RainbowEffect;

typedef struct {
  char baseEffect[16];
  bool show_peaks;
  float hue_offset_low;
  float hue_offset_high;
  float hue_offset_peak;
  float hue_start;
  float hue_end;
  float period;

  float value;
  float saturation;

  bool absolute_range;
  float range_to_max;

  float max_fallback_divider;
  int peak_fallback_rate;

} AudioEffect;

typedef struct {
  bool reverse;

  bool dual_bars;
  
  bool middle_out;

  int bar_1_bin_start;
  int bar_1_bin_end;

  int bar_2_bin_start;
  int bar_2_bin_end;
} AudioBins;

float sigmoid_bin_amplitude(float bin_amplitude);
float normalise_bin_amplitude(float bin_amplitude, int bin_count);


#endif
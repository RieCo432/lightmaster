#include <FastLED.h>
#include "led.h"
#include "element.h"
#include <tuple>


Element::Element() {
  from_pos_x = 0;
  from_pos_y = 0;
  from_pos_z = 0;

  to_pos_x = 0;
  to_pos_y = 0;
  to_pos_z = 0;
      
  num_leds = 0;

  start_led = NULL;
  strip_start = NULL;

  next_led = NULL;
};


Element::Element(float from_x, float from_y, float from_z, float to_x, float to_y, float to_z, int length, Led* first_led, CRGB* strip, float* fft_audio_bins) {
  from_pos_x = from_x;
  from_pos_y = from_y;
  from_pos_z = from_z;

  to_pos_x = to_x;
  to_pos_y = to_y;
  to_pos_z = to_z;
      
  num_leds = length;

  start_led = first_led;
  strip_start = strip;

  audio_bins = fft_audio_bins;

  audio_mask = malloc(num_leds);

  float diff_x = to_pos_x - from_pos_x;
  float diff_y = to_pos_y - from_pos_y;
  float diff_z = to_pos_z - from_pos_z;

  float diff_x_per_led = diff_x / num_leds;
  float diff_y_per_led = diff_y / num_leds;
  float diff_z_per_led = diff_z / num_leds;

  float margin_x = diff_x_per_led / 2;
  float margin_y = diff_y_per_led / 2;
  float margin_z = diff_z_per_led / 2;

  for (int i=0; i < num_leds; i++) {
    start_led[i].pos_x = from_pos_x + i * diff_x_per_led + margin_x;
    start_led[i].pos_y = from_pos_y + i * diff_y_per_led + margin_y;
    start_led[i].pos_z = from_pos_z + i * diff_z_per_led + margin_z;
  };
  next_led = &first_led[num_leds];
};


void Element::setLedOffsets(float offset_x, float offset_y, float offset_z) {
  for (int i=0; i < num_leds; i++) {
    start_led[i].setOffsets(offset_x, offset_y, offset_z);
  };
};

std::tuple<float, float, float, float> Element::setLedApparentAngles() {
  float alpha_min = 0;
  float alpha_max = 0;
  float beta_min = 0;
  float beta_max = 0;
  for (int i=0; i < num_leds; i++) {
    float alpha;
    float beta;

    std::tie(alpha, beta) = start_led[i].setApparentAngles();
    
    if (alpha < alpha_min) {
      alpha_min = alpha;
    } else if (alpha > alpha_max) {
      alpha_max = alpha;
    }
    
    if (beta < beta_min) {
      beta_min = beta;
    } else if (beta > beta_max) {
      beta_max = beta;
    }
  };

  return std::make_tuple(alpha_min, alpha_max, beta_min, beta_max);
};

void Element::closeLedApparentAngles(float factor_alpha, float factor_beta) {
  for (int i=0; i < num_leds; i++) {
    start_led[i].closeApparentAngles(factor_alpha, factor_beta);
  };
};

void Element::setRainbowEffect(RainbowEffect* newRainbowEffect) {
  rainbowEffect = *newRainbowEffect;
};

void Element::applyRainbowBackground() {
  for (int i=0; i < num_leds; i++) {
        strip_start[i] = start_led[i].getRainbowColour(millis(), &rainbowEffect);
      };
}


void Element::applySpectrumBarsBackground() {


  float period = audioEffect.period;
  float hue_start = audioEffect.hue_start / 180 * M_PI;
  float hue_end = audioEffect.hue_end / 180 * M_PI;

  float hue_range = hue_end - hue_start;

  float radians_per_second = period != 0.0 ? 2 * M_PI / period : 0.0;

  float angle_hue_factor = hue_range / (2 * M_PI);

  if (fmodf(hue_range, 2 * M_PI) != 0) {
    angle_hue_factor *= 2;
  }
  

  float final_hue_offset = fmodf((millis() / 1000.0 * radians_per_second) * angle_hue_factor, 2 * M_PI);

  if (fmodf(hue_range, 2 * M_PI) != 0) {
    final_hue_offset = fmodf(final_hue_offset, 2 * abs(hue_range)) + hue_start;
    if (hue_range > 0 && final_hue_offset > hue_end) {
      float excess_angle = final_hue_offset - hue_end;
      final_hue_offset = hue_end - excess_angle;
    } else if (hue_range < 0 && final_hue_offset < hue_end) {
      float gap_angle = hue_end - final_hue_offset;
      final_hue_offset = hue_end + gap_angle;
    }
  }

  int saturation_255 = round(audioEffect.saturation * 255);
  int value_255 = round(audioEffect.value * 255);

  float hue_offset_low = audioEffect.hue_offset_low / 180 * M_PI;
  float hue_offset_high = audioEffect.hue_offset_high / 180 * M_PI;
  float hue_offset_peak = audioEffect.hue_offset_peak / 180 * M_PI;


  float hue_low = fmodf(final_hue_offset + audioEffect.hue_offset_low / 180 * M_PI, 2 * M_PI);
  float hue_high = fmodf(final_hue_offset + audioEffect.hue_offset_high / 180 * M_PI, 2* M_PI);
  float hue_peak = fmodf(final_hue_offset + audioEffect.hue_offset_peak / 180 * M_PI, 2* M_PI);

  int max_num_leds;

  int hues_255[num_leds];

  if (!audioEffect.dual_bars) {
    if (audioEffect.absolute_range) {
      max_num_leds = round(audioEffect.range_to_max);
    } else {
      max_num_leds = round(num_leds * audioEffect.range_to_max);
    }

    float hue_radians_shift_per_led = (hue_offset_high - hue_offset_low) / max_num_leds;

    for (int i=0; i < max_num_leds; i++) {
      hues_255[i] = round((hue_low + i * hue_radians_shift_per_led) / (2 * M_PI) * 255);
    };
    for (int i=max_num_leds; i < num_leds; i++) {
      hues_255[i] = round(hue_high / (2 * M_PI) * 255);
    };
    if (audioEffect.show_peaks) hues_255[bar_1_peak_index] = round(hue_peak / (2 * M_PI) * 255);

    if (!audioEffect.reverse) {
      for (int i=0; i < num_leds; i++) {
        strip_start[i] = CHSV(hues_255[i], saturation_255, value_255);
      };
    } else {
      for (int i=0; i < num_leds; i++) {
        strip_start[num_leds - 1 - i] = CHSV(hues_255[i], saturation_255, value_255);
      }
    }
  } else if (audioEffect.dual_bars) {

    if (audioEffect.absolute_range) {
      max_num_leds = round(audioEffect.range_to_max);
    } else {
      max_num_leds = ceil(num_leds / 2 * audioEffect.range_to_max);
    }

    float hue_radians_shift_per_led = (hue_offset_high - hue_offset_low) / max_num_leds;


    int bar_1_index_offset = floor(num_leds / 2 - 0.5);
    int bar_2_index_offset = ceil(num_leds / 2 - 0.5);

    if (!audioEffect.middle_out) {
      for (int i=0; i < max_num_leds; i++) {
        hues_255[i] = round((hue_low + i * hue_radians_shift_per_led) / (2 * M_PI) * 255);
      };
      for (int i=max_num_leds; i <= bar_1_index_offset; i++) {
        hues_255[i] = round(hue_high / (2 * M_PI) * 255);
      };
      if (audioEffect.show_peaks) hues_255[bar_1_peak_index] = round(hue_peak / (2 * M_PI) * 255);


      for (int i=0; i < max_num_leds; i++) {
        hues_255[num_leds - 1 - i] = round((hue_low + i * hue_radians_shift_per_led) / (2 * M_PI) * 255);
      };
      for (int i=max_num_leds; i <= bar_2_index_offset; i++) {
        hues_255[num_leds - 1 - i] = round(hue_high / (2 * M_PI) * 255);
      };
      if (audioEffect.show_peaks) hues_255[num_leds - 1 - bar_2_peak_index] = round(hue_peak / (2 * M_PI) * 255);


    } else if (audioEffect.middle_out) {

      for (int i=0; i < max_num_leds; i++) {
        hues_255[bar_1_index_offset - i] = round((hue_low + i * hue_radians_shift_per_led) / (2 * M_PI) * 255);
      };
      for (int i=max_num_leds; i <= bar_1_index_offset; i++) {
        hues_255[bar_1_index_offset - i] = round(hue_high / (2 * M_PI) * 255);
      };
      if (audioEffect.show_peaks) hues_255[bar_1_index_offset - bar_1_peak_index] = round(hue_peak / (2 * M_PI) * 255);


      for (int i=bar_2_index_offset; i < bar_2_index_offset + max_num_leds; i++) {
        hues_255[i] = round((hue_low + (i - bar_2_index_offset) * hue_radians_shift_per_led) / (2 * M_PI) * 255);
      };
      for (int i=bar_2_index_offset + max_num_leds; i < num_leds; i++) {
        hues_255[i] = round(hue_high / (2 * M_PI) * 255);
      };
      if (audioEffect.show_peaks) hues_255[bar_2_index_offset - bar_2_peak_index] = round(hue_peak / (2 * M_PI) * 255);
    }

    for (int i=0; i < num_leds; i++) {
        strip_start[i] = CHSV(hues_255[i], saturation_255, value_255);
    };
  }
}

void Element::calculateAudioMask() {

  for (int i=0; i < num_leds; i++) {
    audio_mask[i] = false;
  }

  float bar_1_amplitude = 0.0;
  for (int i=audioEffect.bar_1_bin_start; i <= audioEffect.bar_1_bin_end; i++) {
    bar_1_amplitude += audio_bins[i];
  }
  //bar_1_amplitude /= (audioEffect.bar_1_bin_end - audioEffect.bar_1_bin_start);


  float normalised_bar_1_amplitude = normalise_bin_amplitude(bar_1_amplitude);
  int bar_1_max_led_count = num_leds;

  float bar_2_amplitude;
  float normalised_bar_2_amplitude;
  int bar_2_max_led_count;

  if (audioEffect.dual_bars) {
    bar_2_amplitude = 0.0;
    for (int i=audioEffect.bar_2_bin_start; i <= audioEffect.bar_2_bin_end; i++) {
      bar_2_amplitude += audio_bins[i];
    }
    //bar_2_amplitude /= (audioEffect.bar_2_bin_end - audioEffect.bar_2_bin_start);

    normalised_bar_2_amplitude = normalise_bin_amplitude(bar_2_amplitude);
    bar_1_max_led_count = floor(num_leds / 2);
    bar_2_max_led_count = bar_1_max_led_count;
  }


  int bar_1_led_count_target = round(bar_1_max_led_count * normalised_bar_1_amplitude);
  bar_1_max_index = max(bar_1_led_count_target, round(bar_1_max_index / audioEffect.max_fallback_divider));
  bar_1_peak_index = max(max(bar_1_peak_index - audioEffect.peak_fallback_rate, 0), bar_1_led_count_target);


  /*Serial.print("amplitude 1: ");
  Serial.print(bar_1_amplitude);
  Serial.print("; normal 1: ");
  Serial.print(normalised_bar_1_amplitude);
  Serial.print("; count_target 1: ");
  Serial.print(bar_1_led_count_target);
  Serial.print("; max 1: ");
  Serial.print(bar_1_max_index);
  Serial.print("; peak 1: ");
  Serial.println(bar_1_peak_index);*/
  
  int bar_2_led_count_target;

  if (audioEffect.dual_bars) {
    bar_2_led_count_target = round(bar_2_max_led_count * normalised_bar_2_amplitude);

    bar_2_max_index = max(bar_2_led_count_target, round(bar_2_max_index / audioEffect.max_fallback_divider));
    bar_2_peak_index = max(max(bar_2_peak_index - audioEffect.peak_fallback_rate, 0), bar_2_led_count_target);
  }


  /*Serial.print("amplitude 2: ");
  Serial.print(bar_2_amplitude);
  Serial.print("; normal 2: ");
  Serial.print(normalised_bar_2_amplitude);
  Serial.print("; count_target 2: ");
  Serial.print(bar_2_led_count_target);
  Serial.print("; max 2: ");
  Serial.print(bar_2_max_index);
  Serial.print("; peak 2: ");
  Serial.println(bar_2_peak_index);*/

  if (!audioEffect.dual_bars) {

    if (!audioEffect.reverse) {
      audio_mask[bar_1_peak_index] = audioEffect.show_peaks;
      for (int i=0; i <= bar_1_max_index; i++) {
        audio_mask[i] = true;
      }

    } else if (audioEffect.reverse) {
      audio_mask[num_leds - 1 - bar_1_peak_index] = audioEffect.show_peaks;
      for (int i=0; i <= bar_1_max_index; i++) {
        audio_mask[num_leds - 1 - i] = true;
      }
    }  
    
  } else if (audioEffect.dual_bars) {

    if (!audioEffect.middle_out) {

      audio_mask[bar_1_peak_index] = audioEffect.show_peaks;
      for (int i=0; i <= bar_1_max_index; i++) {
        audio_mask[i] = true;
      }
      
      audio_mask[num_leds - 1 - bar_2_peak_index] = audioEffect.show_peaks;
      for (int i=0; i <= bar_2_max_index; i++) {
        audio_mask[num_leds - 1 - i] = true;
      }

    } else if (audioEffect.middle_out) {

      int bar_1_start = floor(num_leds / 2 - 0.5);
      int bar_2_start = ceil(num_leds / 2 - 0.5);

      audio_mask[bar_1_start - bar_1_peak_index] = audioEffect.show_peaks;
      for (int i=0; i <= bar_1_max_index; i++) {
        audio_mask[bar_1_start - i] = true;
      }

      audio_mask[bar_2_start + bar_2_peak_index] = audioEffect.show_peaks;
      for (int i=0; i <= bar_2_max_index; i++) {
        audio_mask[bar_2_start + i] = true;
      }
    }
  }
}

void Element::applyAudioMask() {
  for (int i=0; i < num_leds; i++) {
    if (!audio_mask[i]) strip_start[i] = CRGB::Black;
  }
};

void Element::setStripColours() {
  // effect selection happens here, then call relevant Led methods if necessary
  if (!effect.enabled) {
    for (int i=0; i < num_leds; i++) {
      strip_start[i] = CRGB::Black;
    };
  } else {
    if (strcmp(effect.name, "rainbow") == 0) {

      applyRainbowBackground();
      
    } else if (strcmp(effect.name, "audio") == 0) {

      calculateAudioMask();

      if (strcmp(audioEffect.baseEffect, "rainbow") == 0) {
        applyRainbowBackground();
      } else if (strcmp(audioEffect.baseEffect, "spectrumBars") == 0) {
        applySpectrumBarsBackground();
      }

      applyAudioMask();
    };
  }
}
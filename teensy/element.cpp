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


Element::Element(float from_x, float from_y, float from_z, float to_x, float to_y, float to_z, int length, Led* first_led, CRGB* strip) {
  from_pos_x = from_x;
  from_pos_y = from_y;
  from_pos_z = from_z;

  to_pos_x = to_x;
  to_pos_y = to_y;
  to_pos_z = to_z;
      
  num_leds = length;

  start_led = first_led;
  strip_start = strip;

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
}


void Element::resetActiveRainbowEffect() {
  activeRainbowEffect = &rainbowEffect;
}


void Element::setActiveRainbowEffect(RainbowEffect* newActiveRainbowEffect) {
  activeRainbowEffect = newActiveRainbowEffect;
};

void Element::setStripColours() {
  // effect selection happens here, then call relevant Led methods if necessary
  for (int i=0; i < num_leds; i++) {
    strip_start[i] = start_led[i].getRainbowColour(millis(), activeRainbowEffect);
  };
}
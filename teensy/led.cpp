#include <tuple>
#include <FastLED.h>
#include "led.h"
#include <math.h>
#include "config.h"


Led::Led() {
  pos_x = 0;
  pos_y = 0;
  pos_z = 0;
}

Led::Led(float x, float y, float z) {
  pos_x = x;
  pos_y = y;
  pos_z = z;
};

void Led::getPositionString(char* buffer) {
  sprintf(buffer, "x=%f, y=%f, z=%f; ", pos_x, pos_y, pos_z); 
};


void Led::getApparentPositionString(char* buffer) {
  sprintf(buffer, "x=%f, y=%f, z=%f; ", apparent_pos_x, apparent_pos_y, apparent_pos_z); 
};


void Led::getApparentAnglesString(char* buffer) {
  sprintf(buffer, "alpha=%f, beta=%f; ", apparent_angle_alpha, apparent_angle_beta); 
};


void Led::setOffsets(float x, float y, float z) {
  offset_x = x;
  offset_y = y;
  offset_z = z;
};


void Led::setViewer(float viewer_x, float viewer_y, float viewer_z) {
  apparent_pos_x = pos_x + offset_x - viewer_x;
  apparent_pos_y = pos_y + offset_y - viewer_y;
  apparent_pos_z = pos_z + offset_z - viewer_z;
};


std::tuple<float, float> Led::setApparentAngles() {
  if (apparent_pos_y >= 0) {
    apparent_angle_alpha = fmodf(2 * M_PI + atan(apparent_pos_x / apparent_pos_y), 2 * M_PI);
  } else {
    apparent_angle_alpha = fmodf(M_PI + atan(apparent_pos_x / apparent_pos_y), 2 * M_PI);
  };
  
  apparent_angle_beta = fmodf(atan2(apparent_pos_z, sqrt(pow(apparent_pos_x, 2.0) + pow(apparent_pos_y, 2.0))), M_PI / 2);
  return std::make_tuple(apparent_angle_alpha, apparent_angle_beta);
}

void Led::closeApparentAngles(float factor_alpha, float factor_beta) {
  apparent_angle_alpha *= factor_alpha;
  apparent_angle_beta *= factor_beta;
}

CRGB Led::getRainbowColour(uint32_t time_elapsed, RainbowEffect* rainbowEffect) {
  float period = rainbowEffect->period;
  float hue_start = rainbowEffect->hue_start / 180 * M_PI;
  float hue_end = rainbowEffect->hue_end / 180 * M_PI;
  int compress = rainbowEffect->compress;

  float hue_range = hue_end - hue_start;

  float angle = rainbowEffect->direction == 0 ? apparent_angle_alpha : apparent_angle_beta;
  float radians_per_second = period != 0.0 ? 2 * M_PI / period : 0.0;

  float angle_hue_factor = hue_range / (2 * M_PI);

  if (fmodf(hue_range, 2 * M_PI) != 0) {
    angle_hue_factor *= 2;
  }
  

  float final_angle = (angle + time_elapsed / 1000.0 * radians_per_second) * angle_hue_factor * compress;

  if (fmodf(hue_range, 2 * M_PI) != 0) {
    final_angle = fmodf(final_angle, 2 * abs(hue_range)) + hue_start;
    if (hue_range > 0 && final_angle > hue_end) {
      float excess_angle = final_angle - hue_end;
      final_angle = hue_end - excess_angle;
    } else if (hue_range < 0 && final_angle < hue_end) {
      float gap_angle = hue_end - final_angle;
      final_angle = hue_end + gap_angle;
    }
  }

  int hue_255 = round(final_angle /  (2 * M_PI) * 255);
  int saturation_255 = round(255 * rainbowEffect->saturation);
  int value_255 = round(255 * rainbowEffect->value);

  return CHSV(hue_255, saturation_255, value_255);
}

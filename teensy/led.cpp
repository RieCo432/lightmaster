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

  apparent_pos_x = pos_x - offset_x;
  apparent_pos_y = pos_y - offset_y;
  apparent_pos_z = pos_z - offset_z;
};


std::tuple<float, float> Led::setApparentAngles() {
  apparent_angle_alpha = fmodf(atan2(apparent_pos_x, apparent_pos_y) + 2 * M_PI, 2 * M_PI);
  apparent_angle_beta = fmodf(atan2(apparent_pos_z, sqrt(pow(apparent_pos_x, 2.0) + pow(apparent_pos_y, 2.0))), M_PI / 2);
  return std::make_tuple(apparent_angle_alpha, apparent_angle_beta);
}

void Led::closeApparentAngles(float factor_alpha, float factor_beta) {
  apparent_angle_alpha *= factor_alpha;
  apparent_angle_beta *= factor_beta;
}

CRGB Led::getRainbowColour(uint32_t time_elapsed, RainbowEffect* rainbowEffect) {
  float period = rainbowEffect->period;

  float angle = rainbowEffect->direction == 0 ? apparent_angle_alpha : apparent_angle_beta;
  float radians_per_second = 2 * M_PI / period;

  float final_angle = angle + time_elapsed / 1000.0 * radians_per_second;
  int angle_255 = round(final_angle /  (2 * M_PI) * 255);
  return CHSV(angle_255, 255, 255);
}

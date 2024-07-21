#include <FastLED.h>
#include "led.h"


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
  sprintf(buffer, "x=%f, y=%f, z=%f; ", pos_x - offset_x, pos_y - offset_y, pos_z - offset_z); 
};


void Led::setOffsets(float x, float y, float z) {
  offset_x = x;
  offset_y = y;
  offset_z = z;
}

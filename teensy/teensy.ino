#include "led.h"
#include "element.h"
#include "container.h"
#include <FastLED.h>


#define HWSerial Serial1
#define POINTER_SIZE 4

#define NUM_LEDS 790
#define NUM_ELEMENTS 8

#define DATA_PIN 11
#define CLOCK_PIN 13



CRGB strip[NUM_LEDS];
Led leds[NUM_LEDS] = {};
Element elements[NUM_ELEMENTS] = {};
Container room;



void setup() {
  FastLED.addLeds<WS2801, DATA_PIN, CLOCK_PIN, RGB>(strip, NUM_LEDS);

  float min_x = 0.0;
  float max_x = 4.75;

  float min_y = 0.0;
  float max_y = 3.35;

  float min_z = 0.40;
  float max_z = 2.50;

  elements[0] = Element(min_x, max_y, min_z, min_x, max_y, max_z, 69, &leds[0]);
  elements[1] = Element(min_x, max_y, max_z, max_x, max_y, max_z, 149, &leds[69]);
  elements[2] = Element(max_x, max_y, min_z, max_x, max_y, max_z, 69, &leds[218]);
  elements[3] = Element(max_x, max_y, max_z, max_x, min_y, max_z, 108, &leds[287]);
  elements[4] = Element(max_x, min_y, min_z, max_x, min_y, max_z, 69, &leds[395]);
  elements[5] = Element(max_x, min_y, max_z, min_x, min_y, max_z, 149, &leds[464]);
  elements[6] = Element(min_x, min_y, min_z, min_x, min_y, max_z, 69, &leds[613]);
  elements[7] = Element(min_x, min_y, max_z, min_x, max_y, max_z, 108, &leds[682]);

  room = Container(8, &elements[0], 2.37, 1.67, 1.7);
  room.setElementOffsets();
  room.setElementApparentAngles();
}

void loop() {
  // put your main code here, to run repeatedly:
  for (int i=0; i < NUM_LEDS; i++) {
    /*char buf1[36];
    leds[i].getPositionString(buf1);
    Serial.print(buf1);
    char buf2[36];
    leds[i].getApparentPositionString(buf2);
    Serial.print(buf2);
    char buf3[36];
    leds[i].getApparentAnglesString(buf3);
    Serial.println(buf3);*/

    strip[i] = leds[i].getColour(millis());
  };
  FastLED.show();
}

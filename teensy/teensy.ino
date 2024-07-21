#include "led.h"
#include "element.h"
#include "container.h"
#include <FastLED.h>


#define HWSerial Serial1
#define POINTER_SIZE 4

#define NUM_LEDS 20
#define NUM_ELEMENTS 4

#define DATA_PIN 11
#define CLOCK_PIN 13



CRGB strip[NUM_LEDS];
Led leds[NUM_LEDS] = {};
Element elements[NUM_ELEMENTS] = {};
Container table;



void setup() {
  // put your setup code here, to run once:
  //
  //FastLED.addLeds<WS2801, DATA_PIN, CLOCK_PIN, RGB>(leds, NUM_LEDS);
  //
  /*Element first_line = 
  Element second_line = 
  Element third_line = 
  Element fourth_line = */

  elements[0] = Element(0, 0, 0, 5, 0, 0, 5, &leds[0]);
  elements[1] = Element(5, 0, 0, 5, 5, 0, 5, &leds[5]);
  elements[2] = Element(5, 5, 0, 0, 5, 0, 5, &leds[10]);
  elements[3] = Element(0, 5, 0, 0, 0, 0, 5, &leds[15]);

  table = Container(4, &elements[0], 2.5, 2.5, 0);
  table.setElementOffsets();
}

void loop() {
  // put your main code here, to run repeatedly:
  for (int i=0; i < NUM_LEDS; i++) {
    char buf1[36];
    leds[i].getPositionString(buf1);
    Serial.print(buf1);
    char buf2[36];
    leds[i].getApparentPositionString(buf2);
    Serial.println(buf2);
  };
  delay(1000);

}

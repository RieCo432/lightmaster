#include "led.h"
#include "element.h"
#include "container.h"
#include <FastLED.h>
#include <Audio.h>


#define HWSerial Serial1
#define POINTER_SIZE 4

#define NUM_LEDS 790
#define NUM_ELEMENTS 8

#define DATA_PIN 11
#define CLOCK_PIN 13


AudioInputAnalog       input;
AudioAnalyzeFFT1024    fft;
AudioOutputI2S         audioOutput;        // audio shield: headphones & line-out

AudioConnection patchCord1(input, 0, fft, 0);

const int myInput = AUDIO_INPUT_LINEIN;


CRGB strip[NUM_LEDS];
Led leds[NUM_LEDS] = {};
Element elements[NUM_ELEMENTS] = {};
Container room;


float audio_bins[512];



void setup() {

  AudioMemory(12);

  FastLED.addLeds<WS2801, DATA_PIN, CLOCK_PIN, RGB>(strip, NUM_LEDS);

  float min_x = 0.0;
  float max_x = 4.75;

  float min_y = 0.0;
  float max_y = 3.35;

  float min_z = 0.40;
  float max_z = 2.50;

  elements[0] = Element(min_x, max_y, min_z, min_x, max_y, max_z, 69, &leds[0], &strip[0], audio_bins);
  elements[1] = Element(min_x, max_y, max_z, max_x, max_y, max_z, 149, &leds[69], &strip[69], audio_bins);
  elements[2] = Element(max_x, max_y, min_z, max_x, max_y, max_z, 69, &leds[218], &strip[218], audio_bins);
  elements[3] = Element(max_x, max_y, max_z, max_x, min_y, max_z, 108, &leds[287], &strip[287], audio_bins);
  elements[4] = Element(max_x, min_y, min_z, max_x, min_y, max_z, 69, &leds[395], &strip[395], audio_bins);
  elements[5] = Element(max_x, min_y, max_z, min_x, min_y, max_z, 149, &leds[464], &strip[464], audio_bins);
  elements[6] = Element(min_x, min_y, min_z, min_x, min_y, max_z, 69, &leds[613], &strip[613], audio_bins);
  elements[7] = Element(min_x, min_y, max_z, min_x, max_y, max_z, 108, &leds[682], &strip[682], audio_bins);

  room = Container(8, &elements[0], max_x / 2, max_y / 2, 1.7);
  room.setElementOffsets();
  room.setElementApparentAngles();

  for (int i=0; i < NUM_LEDS; i++) {
    strip[i] = CRGB::Black;
  }
  FastLED.show();

}

void loop() {
  // put your main code here, to run repeatedly:
  room.setStripColours();
  FastLED.show();
  if (fft.available()) {
    /*Serial.print(millis());
    Serial.print("; x=");
    Serial.print(fft.read(10));
    Serial.print("; y=");
    Serial.print(fft.read(11));
    Serial.print("; z=");
    Serial.print(fft.read(12));
    Serial.print("; sum=");
    Serial.println(fft.read(10, 12));*/
    for (int i=0; i < 512; i++) {
      audio_bins[i] = fft.read(i);
    }
  }
}

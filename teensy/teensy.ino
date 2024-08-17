#include "led.h"
#include "element.h"
#include "container.h"
#include <FastLED.h>
#include <Audio.h>
#include <ArduinoJson.h>


#define HWSerial Serial1
#define POINTER_SIZE 4

#define NUM_LEDS 922
#define NUM_ELEMENTS 12
#define NUM_CONTAINERS 2

#define DATA_PIN 11
#define CLOCK_PIN 13

#define RX_BUFFER_SIZE 2048


AudioInputAnalog       input;
AudioAnalyzeFFT1024    fft;
AudioOutputI2S         audioOutput;        // audio shield: headphones & line-out

AudioConnection patchCord1(input, 0, fft, 0);

const int myInput = AUDIO_INPUT_LINEIN;

CRGB strip[NUM_LEDS];
Led leds[NUM_LEDS] = {};
Element elements[NUM_ELEMENTS] = {};
Container containers[NUM_CONTAINERS] {};


float audio_bins[512];



void setup() {
  HWSerial.setTX(1);
  HWSerial.setRX(0);
  HWSerial.begin(9600);

  AudioMemory(12);

  FastLED.addLeds<WS2801, DATA_PIN, CLOCK_PIN, RGB>(strip, NUM_LEDS);

  float room_min_x = 0.0;
  float room_max_x = 4.75;

  float room_min_y = 0.0;
  float room_max_y = 3.35;

  float room_min_z = 0.40;
  float room_max_z = 2.50;

  float table_min_x = 0.0;
  float table_max_x = 1.28;

  float table_min_y = 0.0;
  float table_max_y = 0.78;

  float table_z = 0.0;

  elements[0] = Element(room_min_x, room_max_y, room_min_z, room_min_x, room_max_y, room_max_z, 69, &leds[0], &strip[0], audio_bins);
  elements[1] = Element(room_min_x, room_max_y, room_max_z, room_max_x, room_max_y, room_max_z, 149, &leds[69], &strip[69], audio_bins);
  elements[2] = Element(room_max_x, room_max_y, room_min_z, room_max_x, room_max_y, room_max_z, 69, &leds[218], &strip[218], audio_bins);
  elements[3] = Element(room_max_x, room_max_y, room_max_z, room_max_x, room_min_y, room_max_z, 108, &leds[287], &strip[287], audio_bins);
  elements[4] = Element(room_max_x, room_min_y, room_min_z, room_max_x, room_min_y, room_max_z, 69, &leds[395], &strip[395], audio_bins);
  elements[5] = Element(room_max_x, room_min_y, room_max_z, room_min_x, room_min_y, room_max_z, 149, &leds[464], &strip[464], audio_bins);
  elements[6] = Element(room_min_x, room_min_y, room_min_z, room_min_x, room_min_y, room_max_z, 69, &leds[613], &strip[613], audio_bins);
  elements[7] = Element(room_min_x, room_min_y, room_max_z, room_min_x, room_max_y, room_max_z, 108, &leds[682], &strip[682], audio_bins);


  elements[8] = Element(table_min_x, table_max_y, table_z, table_max_x, table_max_y, table_z, 41, &leds[790], &strip[790], audio_bins);
  elements[9] = Element(table_max_x, table_max_y, table_z, table_max_x, table_min_y, table_z, 25, &leds[831], &strip[831], audio_bins);
  elements[10] = Element(table_max_x, table_min_y, table_z, table_min_x, table_min_y, table_z, 41, &leds[856], &strip[856], audio_bins);
  elements[11] = Element(table_min_x, table_min_y, table_z, table_min_x, table_max_y, table_z, 25, &leds[897], &strip[897], audio_bins);


  containers[0] = Container(8, &elements[0]);
  containers[0].setOffsets(0, 0, 0);
  containers[0].setViewer(2.375, 1.675, 1.6);
  containers[0].setElementApparentAngles();

  containers[1] = Container(4, &elements[8]);
  containers[1].setOffsets(0.1, 1.43, 0.73);
  containers[1].setViewer(2.375, 1.675, 1.6);
  containers[1].setElementApparentAngles();

  for (int i=0; i < NUM_LEDS; i++) {
    strip[i] = CRGB::Black;
  }
  FastLED.show();

}

void loop() {

  if (fft.available()) {
    for (int i=0; i < 512; i++) {
      audio_bins[i] = fft.read(i);
    }
  }

  
  if (HWSerial.available()) {
    char rx_data[RX_BUFFER_SIZE];
    HWSerial.readBytesUntil('\n', rx_data, RX_BUFFER_SIZE);
    Serial.println(rx_data);

    JsonDocument serial_config;
    deserializeJson(serial_config, rx_data);
    
    const char* target_type = new char(12);
    const char* target_config = new char(12);


    target_type = serial_config["target"];
    int target_index = serial_config["index"];
    target_config = serial_config["type"];

    if (strcmp(target_type, "element") == 0) {
      if (strcmp(target_config, "effect") == 0) {
        elements[target_index].setEffect(serial_config["data"]);
      } else if (strcmp(target_config, "audio") == 0) {
        elements[target_index].setAudioEffect(serial_config["data"]);
      } else if (strcmp(target_config, "rainbow") == 0) {
        elements[target_index].setRainbowEffect(serial_config["data"]);
      } else if (strcmp(target_config, "spectrum_bars") == 0) {
        elements[target_index].setSpectrumBars(serial_config["data"]);
      } else if (strcmp(target_config, "audio_bins") == 0) {
        elements[target_index].setAudioBins(serial_config["data"]);
      }
    }
  }

  for (int i=0; i < NUM_CONTAINERS; i++) {
    containers[i].setStripColours();
  }

  FastLED.show();
}

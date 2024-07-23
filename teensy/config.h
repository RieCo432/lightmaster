#ifndef CONFIG_H
#define CONFIG_H


typedef struct {
  bool enabled;
  float brightness;
  char name[24];
} Effect;


typedef struct {
  float period;
  float hue_start;
  float hue_end;
  int direction;  // 0 = horizontal, 1 = vertical
  int compress; // how many times is the pattern repeated
} RainbowEffect;




#endif
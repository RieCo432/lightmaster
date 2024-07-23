#ifndef CONFIG_H
#define CONFIG_H

typedef struct {
  float period;
  float hue_start;
  float hue_end;
  int direction;  // 0 = horizontal, 1 = vertical
  int compress; // how many times is the pattern repeated
} RainbowEffect;


#endif
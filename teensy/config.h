#ifndef CONFIG_H
#define CONFIG_H

typedef struct {
  float period;
  float start_hue;
  float end_hue;
  int direction;  // 0 = horizontal, 1 = vertical
} RainbowEffect;


#endif
#include "config.h"
#include <math.h>

float sigmoid_bin_amplitude(float bin_amplitude) {
  return (2.0 / (1 + exp(-20 * (bin_amplitude)))) - 1.01;
}

float normalise_bin_amplitude(float bin_amplitude, int bin_range) {
  return bin_amplitude * (1 + (bin_range / 128));
}
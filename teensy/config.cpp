#include "config.h"
#include <math.h>

float normalise_bin_amplitude(float bin_amplitude) {
  return (2.0 / (1 + exp(-70 * pow(bin_amplitude, 2.0)))) - 1;
}
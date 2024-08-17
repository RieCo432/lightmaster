#include "config.h"
#include <math.h>

float normalise_bin_amplitude(float bin_amplitude) {
  return (2.0 / (1 + exp(-18 * bin_amplitude))) - 1;
}
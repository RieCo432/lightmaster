#include "container.h"
#include "element.h"
#include <tuple>
#include <math.h>


Container::Container() {
  num_elements = 0;
  start_element = NULL;

  origin_x = 0;
  origin_y = 0;
  origin_z = 0;
}

Container::Container(int number_of_elements, Element *first_element, float viewer_x, float viewer_y, float viewer_z) {
  num_elements = number_of_elements;
  start_element = first_element;

  origin_x = viewer_x;
  origin_y = viewer_y;
  origin_z = viewer_z;

  for (int i=0; i < number_of_elements; i++) {
    first_element[i].activeRainbowEffect = &rainbowEffect;
    first_element[i].setActiveRainbowEffect(&rainbowEffect);
  }

}

void Container::setElementOffsets() {
  for (int i=0; i < num_elements; i++) {
    start_element[i].setLedOffsets(origin_x, origin_y, origin_z);
  }
}

void Container::setElementApparentAngles() {
  float alpha_min = 0;
  float alpha_max = 0;
  float beta_min = 0;
  float beta_max = 0;

  for (int i=0; i < num_elements; i++) {
    float element_alpha_min;
    float element_alpha_max;
    float element_beta_min;
    float element_beta_max;


    std::tie(element_alpha_min, element_alpha_max, element_beta_min, element_beta_max) = start_element[i].setLedApparentAngles();

    if (element_alpha_min < alpha_min) {
      alpha_min = element_alpha_min;
    };
    
    if (element_alpha_max > alpha_max) {
      alpha_max = element_alpha_max;
    };

    if (element_beta_min < beta_min) {
      beta_min = element_beta_min;
    };

    if (element_beta_max > beta_max) {
      beta_max = element_beta_max;
    };
  };

  float range_alpha = alpha_max - alpha_min;
  float range_beta = beta_max - beta_min;

  float factor_alpha = 2 * M_PI / range_alpha;
  float factor_beta = 2 * M_PI / range_beta;

  for (int i=0; i < num_elements; i++) {
    start_element[i].closeLedApparentAngles(factor_alpha, factor_beta);
  };
}

void Container::setElementRainbowEffect() {
  for (int i=0; i < num_elements; i++) {
    start_element[i].setActiveRainbowEffect(&rainbowEffect);
  }
}


void Container::resetElementRainbowEffect() {
  for (int i=0; i < num_elements; i++) {
    start_element[i].resetActiveRainbowEffect();
  }
}

void Container::setStripColours() {
  for (int i=0; i < num_elements; i++) {
    start_element[i].setStripColours();
  }
}
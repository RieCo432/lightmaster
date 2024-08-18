#include "container.h"
#include "element.h"
#include <tuple>
#include <math.h>


Container::Container() {
  num_elements = 0;
  start_element = NULL;
}

Container::Container(int number_of_elements, Element *first_element) {
  num_elements = number_of_elements;
  start_element = first_element;
  setElementOffsets();
  setElementViewer();
};


void Container::setElementOffsets() {
  for (int i=0; i < num_elements; i++) {
    start_element[i].setLedOffsets(offset_x, offset_y, offset_z);
  }
  setElementApparentAngles();
}

void Container::setElementViewer() {
  for (int i=0; i < num_elements; i++) {
    start_element[i].setLedViewer(viewer_x, viewer_y, viewer_z);
  }
  setElementApparentAngles();
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

    /*Serial.print(i);
    Serial.print(": min: ");
    Serial.print(element_alpha_min / M_PI * 180);
    Serial.print("; max: ");
    Serial.println(element_alpha_max / M_PI * 180);*/


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

  float factor_alpha = 1;  // 2 * M_PI / range_alpha;
  float factor_beta = 2 * M_PI / range_beta;

  for (int i=0; i < num_elements; i++) {
    start_element[i].closeLedApparentAngles(factor_alpha, factor_beta);
  };
}

void Container::setStripColours() {
  for (int i=0; i < num_elements; i++) {
    start_element[i].setStripColours();
  }
}


void Container::setOffsets(float new_offset_x, float new_offset_y, float new_offset_z) {
  offset_x = new_offset_x;
  offset_y = new_offset_y;
  offset_z = new_offset_z;
  setElementOffsets();
}


void Container::setViewer(float new_viewer_x, float new_viewer_y, float new_viewer_z) {
  viewer_x = new_viewer_x;
  viewer_y = new_viewer_y;
  viewer_z = new_viewer_z;
  setElementViewer();
}
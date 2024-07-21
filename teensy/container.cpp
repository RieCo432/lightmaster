#include "container.h"
#include "element.h"


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

}

void Container::setElementOffsets() {
  for (int i=0; i < num_elements; i++) {
    start_element[i].setLedOffsets(origin_x, origin_y, origin_z);
  }
}

void Container::setElementApparentAngles() {
  for (int i=0; i < num_elements; i++) {
    start_element[i].setLedApparentAngles();
  }
}
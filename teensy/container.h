#ifndef CONTAINER_H
#define CONTAINER_H
#include "element.h"

class Container {
  public:
    int num_elements;
    Element *start_element;

    float origin_x;
    float origin_y;
    float origin_z;

    float container_offset_x = 0;
    float container_offset_y = 0;
    float container_offset_z = 0;

    Container();
    Container(int num_of_elements, Element* first_element, float viewer_x, float viewer_y, float viewer_z);

    void setContainerOffsets(float offset_x, float offset_y, float offset_z);
    void setElementOffsets();
    void setElementApparentAngles();
    void setStripColours();
};

#endif
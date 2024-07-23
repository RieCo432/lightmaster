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

    Container();
    Container(int num_of_elements, Element* first_element, float viewer_x, float viewer_y, float viewer_z);

    void setElementOffsets();
    void setElementApparentAngles();
    void setElementRainbowEffect(RainbowEffect* rainbowEffect);
    void setStripColours();
};

#endif
#ifndef CONTAINER_H
#define CONTAINER_H
#include "element.h"

class Container {
  public:
    int num_elements;
    Element *start_element;

    float offset_x = 0;
    float offset_y = 0;
    float offset_z = 0;

    float viewer_x = 0;
    float viewer_y = 0;
    float viewer_z = 0;

    Container();
    Container(int num_of_elements, Element* first_element);

    void setElementViewer();
    void setElementOffsets();
    void setViewer(float new_viewer_x, float new_viewer_y, float new_viewer_z);
    void setOffsets(float new_offset_x, float new_offset_y, float new_offset_z);
    void setElementApparentAngles();
    void setStripColours();
};

#endif
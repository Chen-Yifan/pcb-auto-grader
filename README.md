# pcb-auto-grader
cs543 group project

## [Data Folder](https://github.com/NeoWu1216/pcb-auto-grader/tree/master/data)
Contains raw and processed data for training.  
Data will be converted to png based file.

## [Experiment Folder](https://github.com/NeoWu1216/pcb-auto-grader/tree/master/experiment)
Contains jupyter notebooks that are used to evaluate different detecting method.  
Here is a list of methods we tried:
* Blob feature detector
* Slicing window based detector
* Ground Plane CNN based detector
* Object detector for components detector
* Line detector
* Morphology segmentation
* Morphology erosion
* Tracedetection

## [Grader Folder](https://github.com/NeoWu1216/pcb-auto-grader/tree/master/grader)
Contains code used to calculate grade for a student homework.  
Here is a list of files and its purpose:
```
grader
"""
the function called to grade a student's zipped file
return: a number and a string of grading break down
"""

zip_handling
"""
set up workspace for grading task
finds the workspace if there is a folder embedded in the zip file
exception: if file is not zip
"""

render_gerber
"""
Render the pcb CAD file to an top vew and bottom view image of PCB with correct palette
"""

grade_components
"""
find components on the PCB and classify them to see whether each type of component is present
The info will be used for future grading tasks down the pipeline
"""

grade_ground_plane
"""
detect whether ground plane is present
"""

grade_trace
"""
Generate topology and grade wheter the components are connected correctly
"""


## Video presentation
Click [here](https://www.youtube.com/watch?v=evb0vagDYxQ) to see our final presentation.

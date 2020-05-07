# pcb-auto-grader
cs543 group project

## [Data Folder](https://github.com/NeoWu1216/pcb-auto-grader/tree/master/data)
Contains raw and processed data for training, data will be converted to png based file

## [Experiment Folder](https://github.com/NeoWu1216/pcb-auto-grader/tree/master/experiment)
Contains jupyter notebooks that are used to evaluate different detecting method
Here is a list of methods we tried:
* Blob feature detector
* Slicing window based detector
* Ground Plane CNN based detector
* Network detector

## Grader Folder
Contains code used to calculate grade for a student homework.  
Here is a list of function signatures:
```
grade_main(zip_file_path) 
"""
the function called to grade a student's zipped file
return: a number and a string of grading break down
"""

unzip_to_folder(zip_file_path, folder_name)
"""
set up workspace for grading task
exception: if file is not zip
"""

preprocess_image(folder_name) 
"""
convert image
exception: if missing files or cannot be rendered
"""

common utility functions 
"""
used to read image from path, do numpy array, tensor, PIL image format conversions
"""
```
## Function list for grading tasks 
```
"""
call in sequence
return: 0 or 1 for the score, will be accumulated in total score of student
"""

detect_ground_plane(folder_name)
ensure_bothside_have traces(folder_name)
detect_components_bounding_box(folder_name) 
detect_graph()
detect_traces()
test_connectivity()
```

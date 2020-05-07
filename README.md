# pcb-auto-grader
cs543 group project

### data folder
Contains raw and processed data for training, data will be converted to png based file

### experiment folder
Contains jupyter notebooks that are used to evaluate different detecting method
Here is a list of methods we tried
Blob feature detector
Slicing window based detector
Ground Plane CNN based detector
Network detector

### grader folder
Contains code used to calculate grade for a student homework
Here is a list of function signatures

grade_main(zip_file_path) # the function called to grade a student's zipped file, needs to return a number and a string of grading break down

unzip_to_folder(zip_file_path, folder_name) # set up workspace for grading task # raise exception if file is not zip
preprocess_image(folder_name) # convert image return None # raise exception if missing files or cannot be rendered

common utility functions: # used to read image from path, do numpy array, tensor, PIL image format conversions

## function list for grading tasks, will be called in sequence
Detect_ground_plane(folder_name) # output 0 or 1 for the score, will be accumulated in total score of student
ensure_bothside_have traces(folder_name)
Detect_components(folder_name) # return bounding box for components
detect_graph()
detect_traces()
test_connectivity()


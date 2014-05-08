robot-localization
==================

This project addresses the problem of robot localization in a pre-mapped space, given a dataset consisting solely of photos. We address this problem by identifying known landmarks and calculating the distance to them using triangulation.

To run the entire project which preprocesesses and perspective corrects the images, identifies the shapes, determines the distance from these shapes and localizes:
python test_robot_localization.py

For each robot location, you will see output like this:

triangle triangle
circle circle
square square
pentagon pentagon
[ 45.4905495   47.34547233] (46.0, 48.0) 0.829425274436 1.73591780663 4

This translates to:
shape, estimated shape
[estimated robot location] (actual robot location) error, time, # images to localize from

To run the preprocessing and perspective correction:
python white_rect_finder.py

To test shape identification:
python test_identify_shapes.py

To determine a nonlinear fit for the relationship between distance and image height:
python pixels_regression.py

To generate a the included csv file (PixelsToDistance55.csv) of distance to landmarks vs. image height:
python pixels_to_distance.py


This project utilizes the following libraries:
cv2
NumPy
SciPy
matplotlib

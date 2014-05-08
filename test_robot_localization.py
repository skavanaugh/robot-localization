import cv2
import numpy as np
import glob
import itertools
import time

import white_rect_finder
import identify_shapes
import intersecting_circles
from visualize import Visualize

# we determined this distance function via nonlinear regression in pixels_regression.py
def get_distance(pix):
	a, b, c = 7212.76441, -0.896184332, -0.858164181
	return a*pix**b+c

all_labeled_images = glob.glob('photoset_labeled/cleaned/*/*/*.JPG')
all_locations = {}

# create a dictionary entry for each location where we are trying to localize
for image_name in all_labeled_images:

	image_path = image_name.split('/')
	present_coordinates_string = image_path[2].split(',')
	present_location = (float(present_coordinates_string[0]), \
						float(present_coordinates_string[1]))
	shape_name = image_path[-2]

	if present_location not in all_locations:
		all_locations[present_location] = {}

	all_locations[present_location][shape_name] = image_name


estimate_list = []
actual_list = []
error_list = []

for location in all_locations:
	
	shapes = []
	distances = []

	start = time.time()
	for shape in all_locations[location]:

		image_name = all_locations[location][shape]
		image = cv2.imread(image_name)

		# start2 = time.time()
		cleaned_image, rectangle_coordinates = white_rect_finder.get_white_rectangles(image)[0]
		# elapsed2 = time.time() - start2

		# start3 = time.time()
		estimated_shape = identify_shapes.detect_shape(cleaned_image)
		# elapsed3 = time.time() - start3

		print shape, estimated_shape #, elapsed2, elapsed3

		shapes.append(shape)

		# find y-coordinates of rectangle
		low_y = (rectangle_coordinates[0][1] + rectangle_coordinates[1][1]) / 2.
		high_y = (rectangle_coordinates[2][1] + rectangle_coordinates[3][1]) / 2.

		# find pixel height
		pixels = high_y - low_y

		estimated_distance = get_distance(pixels)

		distances.append(estimated_distance)

	intersection_points = []

	# start4 = time.time()
	for combo in list(itertools.combinations(range(len(shapes)),2)):

		i, j = combo
		
		# find intersections for each combination of two landmarks
		int1, int2 = intersecting_circles.find_circle_intersection(shapes[i],distances[i], \
						shapes[j],distances[j])

		intersection_points.append(int1)
		intersection_points.append(int2)

	
	all_intersections = np.array(intersection_points)
	# print all_intersections

	# localization estimate using intersections from all circles
	estimated_point = intersecting_circles.estimate_location(all_intersections)

	# elapsed4 = time.time() - start4

	error = np.linalg.norm(estimated_point - np.array([location[0], location[1]]))

	elapsed = time.time() - start

	print estimated_point, location, error, elapsed, len(shapes) #, elapsed4

	est_x, est_y = estimated_point[0], estimated_point[1]

	estimate_list.append((est_x, est_y))
	actual_list.append(location)
	# if len(shapes) == 4:
	error_list.append(error)

# print estimate_list
# print actual_list
# print error_list

print "mean error", np.mean(np.array(error_list))
print "max error", np.max(np.array(error_list))
print "min error", np.min(np.array(error_list))

#####################################

v = Visualize()
v.plot_estimate_list(estimate_list)
v.plot_actual_list(actual_list)
v.show()


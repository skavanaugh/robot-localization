import white_rect_finder
import cv2
import glob
import numpy as np
import csv

triangle_location = np.array([92., 48.])
pentagon_location = np.array([0., 48.])
square_location = np.array([46., 96.])
circle_location = np.array([46., 0.])

shape_name_to_coordinates = {"triangle": triangle_location, "pentagon": pentagon_location,
						"square": square_location, "circle": circle_location}

all_labeled_images = glob.glob('photoset_labeled/cleaned/*/*/*.JPG')

pixels_to_distance = []

for image_name in all_labeled_images:

	image_dict = {}
	image_path = image_name.split('/')

	# find out which shape the image is, map the shape to its location
	# then find distance from present location to the shape landmark
	for shape in shape_name_to_coordinates:
		
		if shape in image_path:
		
			shape_coordinates = shape_name_to_coordinates[shape]
			present_coordinates_string = image_path[2].split(',')
			present_coordinates = np.array([float(present_coordinates_string[0]),
											float(present_coordinates_string[1])])
			distance = np.linalg.norm(shape_coordinates - present_coordinates)
			break

	image = cv2.imread(image_name)

	rectangle_coordinates = white_rect_finder.get_white_rectangles(image, DEBUG=False)[0][1]

	# find y-coordinates of rectangle
	low_y = (rectangle_coordinates[0][1] + rectangle_coordinates[1][1]) / 2.
	high_y = (rectangle_coordinates[2][1] + rectangle_coordinates[3][1]) / 2.

	# find pixel height
	pixels = high_y - low_y

	# print pixels, distance, shape, image_path[-1]
	image_dict["pixels"], image_dict["distance"], image_dict["shape"], image_dict["filename"] = \
			pixels, distance, shape, image_path[-1]

	pixels_to_distance.append(image_dict)


csv_outfile = "PixelsToDistance%s.csv" % len(pixels_to_distance)
fnames = ["pixels", "distance", "shape", "filename"]

with open(csv_outfile, 'wb') as fout:
	writer = csv.DictWriter(fout, fieldnames = fnames, delimiter=',')
	writer.writeheader()
	writer.writerows(pixels_to_distance)






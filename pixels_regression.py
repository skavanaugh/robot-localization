import white_rect_finder
import cv2
import glob
import numpy as np
import csv
from scipy.optimize import curve_fit
import scipy as sy


# this code is used to fit a nonlinear regression curve to be used to map
# image height in pixels to distance in inches



# often initilization of parameters came from Wolfram Alpha using 5-10 points
# as this curve_fit routine would often not converge if given bad initialization parameters

def func(x, a, b, c):
	return a*x**b + c

p0 = np.array([7738.,-0.9123,-0.9])
# [  7.21276441e+03  -8.96184332e-01  -8.58164181e-01]

# below are other types of functions we used to fit the distance vs. image height

# def func(x, a, b, c):
# 	return a*np.log(b*x) + c
# p0 = np.array([-4.78231512e+01,1.26028876e-03,-1.78140080e+00])
# #[ -4.78231512e+01   1.26028876e-03  -1.78140080e+00]

# def func(x, a, b, c):
# 	return a*np.exp(-b*x) + c
# p0 = np.array([1.74622484e+02,7.29575559e-03,2.19700146e+01])
# #[  1.74622484e+02   7.29575559e-03   2.19700146e+01]

# # combination of the other nonlinear regression results
# # note that the result is over 98% the first function above
# def func(x, a, b, c):
# 	return a*((-4.78231512e+01)*np.log((1.26028876e-03)*x) + -1.7814008) \
# 		+ b*(1.74622514e+02*np.exp(-(7.29575753e-03)*x) + 2.19700221e+01) \
# 		+ c*(7.21276441e+03*x**(-8.96184332e-01) + -8.58164181e-01)

# p0 = np.array([-2.43570792e-04,1.85042033e-02,9.81741742e-01])


y = np.array([])
x = np.array([])

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
			y = np.append(y,distance)
			break

	image = cv2.imread(image_name)

	rectangle_coordinates = white_rect_finder.get_white_rectangles(image, DEBUG=False)[0][1]

	# find y-coordinates of rectangle
	low_y = (rectangle_coordinates[0][1] + rectangle_coordinates[1][1]) / 2.
	high_y = (rectangle_coordinates[2][1] + rectangle_coordinates[3][1]) / 2.

	# find pixel height
	pixels = high_y - low_y
	x = np.append(x, pixels)

	# print pixels, distance, shape, image_path[-1]
	image_dict["pixels"], image_dict["distance"], image_dict["shape"], image_dict["filename"] = \
			pixels, distance, shape, image_path[-1]

	pixels_to_distance.append(image_dict)


coeffs, matcov = curve_fit(func, x, y, p0)

#print x
#print y
print "coefficients are", coeffs
#print matcov








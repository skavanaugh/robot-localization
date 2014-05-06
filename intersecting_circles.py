# intersection of two circles 
# using method described here -- http://paulbourke.net/geometry/circlesphere/
# intersection of a line and a circle
# using the method described here -- http://mathworld.wolfram.com/Circle-LineIntersection.html

import numpy as np
import math
from scipy.spatial import KDTree
from scipy.cluster.hierarchy import single
from scipy.spatial.distance import pdist

triangle_location = np.array([92, 48])
pentagon_location = np.array([0, 48])
square_location = np.array([46, 96])
circle_location = np.array([46, 0])

shape_name_to_coordinates = {"triangle": triangle_location, "pentagon": pentagon_location,
						"square": square_location, "circle": circle_location}

# the numpy function numpy.sign returns 0 for x = 0 so we created our own helper function
def sgn(x):
	if x < 0:
		return -1
	else:
		return 1

def estimate_location(points): #shape_names, distances):
	
	# finding half as many points which are close to each other to localize
	num_relevant_points = len(points) / 2
	# checking that distance between points is less than length_threshold
	length_threshold = 6
	
	kd = KDTree(points)

	# find a collection of points less than length_threshold apart
	ball = kd.query_ball_tree(kd, length_threshold)
	
	# keep shrinking the length_threshold until we have the correct number of points
	for i in range(1,4):
		
		if len(ball[0]) > num_relevant_points + 1:
			length_threshold = length_threshold - 1
			ball = kd.query_ball_tree(kd, length_threshold)
		else:
			break

	# this needs to be generalized
	if len(points) == 6:
		indices = ball[1]
	else:
		indices = ball[0]

	all_points = points.tolist()
	
	relevant_points = []
	[relevant_points.append(all_points[indices[i]]) for i in range(len(indices))]

	#print relevant_points

	# average of relevant points is used as localization estimate
	estimated_point = np.mean(np.array(relevant_points), axis=0)

	return estimated_point


def find_closest_two_points(points):
	
	# use single link clustering to find closest two points
	p = pdist(points)
	slc = single(p)
	
	return np.array([points[slc[0][0]], points[slc[0][1]]])


def find_circle_line_intersection(P0, r0, P1):
	"""find two nearest points between two non-intersecting circles"""
	
	x_offset, y_offset = P0
	x0, y0 = 0, 0
	x1, y1 = P1

	x1, y1 = x1 - x_offset, y1 - y_offset

	dx = x1 - x0
	dy = y1 - y0
	dr = math.sqrt(dx*dx + dy*dy)

	D = x0*y1 - x1*y0

	delta0 = r0*r0*dr*dr - D*D

	x2 = (D*dy + sgn(dy)*dx*math.sqrt(delta0)) / (dr*dr)
	y2 = (D*dx + math.fabs(dy)*math.sqrt(delta0)) / (dr*dr)

	x3 = (D*dy - sgn(dy)*dx*math.sqrt(delta0)) / (dr*dr)
	y3 = (D*dx - math.fabs(dy)*math.sqrt(delta0)) / (dr*dr)

	x2 += x_offset
	x3 += x_offset
	y2 += y_offset
	y3 += y_offset

	return np.array([[x2, y2], [x3, y3]])


def find_circle_intersection(shape0_name, r0, shape1_name, r1):
	"""calculates points of intersection between two circles with centers
	at known landmark locations and radii r0 and r1"""

	P0 = shape_name_to_coordinates[shape0_name]
	P1 = shape_name_to_coordinates[shape1_name]

	# distance_between_centers
	d = np.linalg.norm(P0 - P1)

	if d > r0 + r1:

		first_circle = find_circle_line_intersection(P0, r0, P1)
		second_circle = find_circle_line_intersection(P1, r1, P0)
		points = np.concatenate((first_circle, second_circle))
		close = find_closest_two_points(points)
		return close


	a = 0.5 * (r0 * r0 - r1 * r1 + d * d ) / d
	P2 = P0 + a * (P1 - P0) / d
	
	h = math.sqrt(r0 * r0 - a * a)

	x0, y0 = P0
	x1, y1 = P1
	x2, y2 = P2

	x3 = x2 + h * (y1 - y0) / d
	y3 = y2 - h * (x1 - x0) / d

	x4 = x2 - h * (y1 - y0) / d
	y4 = y2 + h * (x1 - x0) / d

	return np.array([[x3, y3], [x4, y4]])


if __name__ == "__main__":
	print find_circle_intersection("circle", 60, "square", 60)[0]




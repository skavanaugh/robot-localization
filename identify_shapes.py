# Code snippets from here
# http://en.wikibooks.org/wiki/Applied_Robotics/Sensors_and_Perception/Open_CV/Basic_OpenCV_Tutorial
# Processing triangles in video: http://opencv-srf.blogspot.com/2011/09/object-detection-tracking-using-contours.html
# How to determine shape size in OpenCV http://stackoverflow.com/questions/19098104/python-opencv2-cv2-wrapper-get-image-size
# Shapes from here http://www.ziggityzoom.com/activity/make-basic-shapes-flashcards

import cv2
import numpy
 
def get_shape(contours, image_to_color, show_shape=False):
    min_shape_size = 200
    shape = None
 
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        # print len(approx)
        if len(approx) == 4 and cv2.contourArea(approx) > min_shape_size:
            shape = "Rectangle"
            cv2.drawContours(image_to_color, [cnt], 0, 255,-1)
        elif len(approx) > 13 and cv2.contourArea(approx) > min_shape_size:
            shape = "Circle"
            cv2.drawContours(image_to_color, [cnt], 0, 255,-1)
        elif len(approx) == 3 and cv2.contourArea(approx) > min_shape_size:
            shape = "Triangle"
            cv2.drawContours(image_to_color, [cnt], 0, 255,-1)  
        elif len(approx) == 5 and cv2.contourArea(approx) > min_shape_size:
            shape = "Pentagon"
            cv2.drawContours(image_to_color, [cnt], 0, 255,-1)
        elif len(approx) == 6 and cv2.contourArea(approx) > min_shape_size:
            shape = "Hexagon"
            cv2.drawContours(image_to_color, [cnt], 0, 255,-1)  
    if show_shape: 
        cv2.imshow('image_to_color', image_to_color)
         # When you're done looking at the image, use this to close all windows:            cv2.destroyAllWindows()
         
    return shape
 
##
# Converts an RGB image to grayscale, where each pixel
# now represents the intensity of the original image.
##
def rgb_to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
 
##
# Converts an image into a binary image at the specified threshold.
# All pixels with a value <= threshold become 0, while
# pixels > threshold become 1
def do_threshold(image, threshold = 170):
    (thresh, im_bw) = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY_INV)
    return (thresh, im_bw)
    
##
# Finds the outer contours of a binary image and returns a shape-approximation
# of them. Because we are only finding the outer contours, there is no object
# hierarchy returned.
##
def find_contours(image):
    (contours, hierarchy) = cv2.findContours(image, mode=cv2.cv.CV_RETR_EXTERNAL, method=cv2.cv.CV_CHAIN_APPROX_SIMPLE)
    return contours
 
##
# Creates a new RGB image of the specified size, initially
# filled with black.
##
def new_rgb_image(width, height):
    image = numpy.zeros( (height, width, 3), numpy.uint8)
    return image 
 
##
# Detects the shape in a given image
##
def detect_shape(img_orig, show_shape = False):
    img_copy = img_orig.copy()
    img_gray = rgb_to_gray(img_orig) # Convert img_orig from video camera from RGB to Grayscale
 
    (thresh, img_threshold) = do_threshold(img_gray, 170)
 
    ##################################################### 
    # If you have created a binary image as above and stored it in "img_threshold"
    # the following code will find the contours of your image:
    contours = find_contours(img_threshold)

    shape = get_shape(contours, img_copy, show_shape)
    
    return shape
 
def detect_shapes( image_names ):
    shapes = []
    for image in image_names:
        shape = detect_shape(image, False)
        shapes.append(shape)
    return shapes
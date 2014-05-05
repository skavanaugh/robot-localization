# A short test to verify the shapes are correctly identified

import os
import cv2

from white_rect_finder import get_white_rectangles
from identify_shapes import detect_shape

base_dir = "photoset_labeled/cleaned"
correctly_classified = 0
incorrectly_classified = 0

for dir in os.listdir(base_dir):
    shape_dir = base_dir + "/" + dir
    for shape_folder in os.listdir(shape_dir):
        photo_dir = shape_dir + "/" + shape_folder
        for photo in os.listdir(photo_dir):
            image = cv2.imread(photo_dir + "/" + photo)
            cards = get_white_rectangles(image)
            for card in cards:
                image, corners = card
                shape = detect_shape(image)
                if shape == shape_folder:
                    correctly_classified += 1
                else:
                    shape = detect_shape(image, show_shape=True)
                    incorrectly_classified +=1
                    print "Incorrect:",shape,shape_folder,photo_dir,photo

print "Correct: ", correctly_classified
print "Incorrect: ", incorrectly_classified
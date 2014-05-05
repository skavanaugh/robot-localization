import glob
import cv2

from white_rect_finder import get_white_rectangles
from identify_shapes import detect_shape

def main():
    orig_imgs = glob.glob('photoset/cleaned/*/*.JPG')
    
    for filename in orig_imgs:
        # Find all cards in each image
        image = cv2.imread(filename)
        cards = get_white_rectangles(image)
        for card in cards:
            image, corners = card
            # For each card, detect the shape
            shape = detect_shape(image)
            print shape

if __name__ == "__main__":
    main()
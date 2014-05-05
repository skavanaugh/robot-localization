import cv2
import numpy as np
from math import *
from operator import add
 
import glob
 
# basis: http://opencv-code.com/tutorials/automatic-perspective-correction-for-quadrilateral-objects/
 
 
kernel_size = 5
BLUR = 7
THRESH_C = -60
RECTANGLE_SIZE = (255, 330) # 8.5"x11" * 30dpi
 
 
WINDOW_WIDTH, WINDOW_HEIGHT = (320, 240)
WINDOW_X_OFFSET = 100
WINDOW_Y_OFFSET = 500
 
 
 
 
 
def get_white_rectangles(img, DEBUG = False):
    """Finds and returns white rectangular sheets of 8.5x11 paper, transformed
    to correct for perspective. Returns as a list of images,"""
    height, width, depth = img.shape
    
    ret = []
    # ret structure:
    # [(img, corners)]
    # img is a scaled to 8.5x11 image as a numpy array
    # corners is a list of 4 points of the original coordinates in the image
    # in the order top-left, top-right, bottom-right, bottom-left
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    blur = cv2.GaussianBlur(gray, (BLUR, BLUR), 0)
    
    # get an odd number around half of the smallest dimension
    thresh_blockSize = int(min(height, width) / 4) * 2 + 1
    
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, thresh_blockSize, THRESH_C)
                                   
    # alternate method: global thresholding w/ Otsu algorithm (unreliable)
    #retval, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    thresh_copy = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    debug_display = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # draw contours on debug img in dark green
    cv2.drawContours(debug_display, contours, -1, (0,63,0), 2)
    
    # filter out small contours (1/16 of the smallest dimension square)
    min_contour_size = (min(height, width) / 16)**2
    contours = [x for x in contours if cv2.contourArea(x) > min_contour_size]
    
    # draw filtered contours in bright green
    cv2.drawContours(debug_display, contours, -1, (0,255,0), 1)
    
    quads = []
    
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, cv2.arcLength(cnt, True) * 0.03, True)
        if len(approx) == 4 and cv2.isContourConvex(approx):
            # found a quadrilateral!
            approx = sort_corners(approx)
            # print approx
            quads.append(approx)
    
    RECTANGLE_WIDTH, RECTANGLE_HEIGHT = RECTANGLE_SIZE
    
    # clean up old windows
    if DEBUG:
        for i in range(4):
            cv2.destroyWindow('warp%d' % i)
    
    for i in range(len(quads)):
        corners = quads[i]
        # apply perspective transform
        h = np.array([ [0,0], [RECTANGLE_WIDTH,0],
                       [RECTANGLE_WIDTH, RECTANGLE_HEIGHT], [0, RECTANGLE_HEIGHT] ], np.float32)
        transform = cv2.getPerspectiveTransform(np.array([corners], np.float32), h)
        warp = cv2.warpPerspective(img, transform, RECTANGLE_SIZE)
        
        ret.append((warp, corners))
    
    
    if DEBUG:
        for q in quads:
            # draw found quadrilaterals as red
            # cv2.polylines(img, np.array([q]), True, (0,0,255), thickness=4)
            cv2.polylines(debug_display, np.array([q]), True, (0,0,255), thickness=4)
        
        thresh = thresh_copy
        
        WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
        img = cv2.resize(img, WINDOW_SIZE)
        blur = cv2.resize(blur, WINDOW_SIZE)
        thresh = cv2.resize(thresh, WINDOW_SIZE)
        debug_display = cv2.resize(debug_display, WINDOW_SIZE)
        cv2.imshow('img', img)
        cv2.imshow('blur', blur)
        cv2.imshow('thresh', thresh)
        cv2.imshow('debug_display', debug_display)
        
        img_windows = ['img', 'blur', 'thresh', 'debug_display']
        for i in range(len(img_windows)):
            w = img_windows[i]
            # cv2.resizeWindow(w, WINDOW_WIDTH, WINDOW_HEIGHT)
            cv2.moveWindow(w, WINDOW_X_OFFSET + WINDOW_WIDTH * i, WINDOW_Y_OFFSET)
        
        for i in range(len(ret)):
            w = 'warp%d' % i
            cv2.imshow(w, ret[i][0])
            cv2.moveWindow(w, WINDOW_X_OFFSET + RECTANGLE_WIDTH * i, 60)
            
    return ret
 
 
def sort_corners(corners):
    """sorts a list of corners in top left, top right, bottom right, bottom left order"""
    # determine mass center
    # points that have lower y than mass center are top points, otherwise they are bottom points
    # of two points, lower x is left, other is right
    
    if len(corners[0] == 1):
        # unpack np array
        corners = [(x[0][0], x[0][1]) for x in corners]
    
    center_x, center_y = (0, 0)
    for pt in corners:
        center_x += pt[0]
        center_y += pt[1]
    
    center_x /= len(corners)
    center_y /= len(corners)
    
    center = (center_x, center_y)
    
    top = []
    bot = []
    
    for pt in corners:
        if pt[1] < center[1]:
            top.append(pt)
        else:
            bot.append(pt)
    
    top.sort(key=lambda pt: pt[0])
    bot.sort(key=lambda pt: pt[0], reverse=True)
    
    return top + bot
            
 
    
def main():
    #orig_imgs = ['photoset/cleaned/7,49/IMG_2654.JPG'] # Square, slight angle
    orig_imgs = glob.glob('photoset/cleaned/*/*.JPG')
    
    def img_onchange(x):
        filename = orig_imgs[cv2.getTrackbarPos('img', 'config')]
        img = cv2.imread(filename)
    
        print filename
        ret = get_white_rectangles(img, DEBUG=True)
        for r in ret:
            print r[1] # just the quads
    
    img_windows = ['img', 'blur', 'thresh', 'debug_display']
    for i in range(len(img_windows)):
        w = img_windows[i]
        cv2.resizeWindow(w, WINDOW_WIDTH, WINDOW_HEIGHT)
        cv2.moveWindow(w, WINDOW_X_OFFSET + WINDOW_WIDTH * i, WINDOW_Y_OFFSET)
        
    cv2.namedWindow('config', cv2.WINDOW_AUTOSIZE)
    cv2.resizeWindow('config', 600, 60)
    cv2.createTrackbar('img', 'config', 0, len(orig_imgs), img_onchange)
 
 
    img_onchange(0)
    cv2.waitKey()
 
 
if __name__ == '__main__':
    main()
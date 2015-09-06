import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2
import numpy as np

def nothing(x):
    pass

# Create a black image, a window
img = np.zeros((300, 500, 3), np.uint8)
imgCat = cv2.imread('cat.jpg', 3)
imgCat = cv2.resize(imgCat, (500, 300))

cv2.namedWindow('image')

imgCat[:,:,0] = 0
imgCat[:,:,1] = 0
ra = imgCat

imgCat = cv2.imread('cat.jpg', 3)
imgCat = cv2.resize(imgCat, (500, 300))

imgCat[:,:,0] = 0
imgCat[:,:,2] = 0
ga = imgCat

imgCat = cv2.imread('cat.jpg', 3)
imgCat = cv2.resize(imgCat, (500, 300))

imgCat[:,:,1] = 0
imgCat[:,:,2] = 0
ba = imgCat


# create trackbars for color change
cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)

cv2.imshow('image',img)
r,g,b = (0,)*3

while(1):
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    r0 = cv2.getTrackbarPos('R','image')
    g0 = cv2.getTrackbarPos('G','image')
    b0 = cv2.getTrackbarPos('B','image')

    if r != r0 or g != g0 or b != b0 :
        r = r0
        g = g0
        b = b0

        _ra = (ra * (r / 255.)).astype('uint8')
        _ga = (ga * (g / 255.)).astype('uint8')
        _ba = (ba * (b / 255.)).astype('uint8')

        img = _ra + _ga + _ba
        cv2.imshow('image', img)


cv2.destroyAllWindows()

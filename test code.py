#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np

img = cv.imread('/Users/arjunmalik/Downloads/uas takimages/1.png')
#cv.imshow("original image", img)

#converting BGR to HSV
img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)   
#cv.imshow("img hsv", img_hsv)    


#masking blue
lower_blue = np.array([15, 100, 180])
upper_blue = np.array([135,255,255])
mask_blue = cv.inRange(img_hsv, lower_blue, upper_blue)
#cv.imshow("mask blue", mask_blue)

#masking red ( unburnt grass)
lower_red = np.array([0,170,170])
upper_red = np.array([10,255,255])
mask_red = cv.inRange(img_hsv, lower_red, upper_red)
#cv.imshow("mask red", mask_red)

#masking green
lower_green = np.array([35, 40, 32])
upper_green = np.array([75, 255, 255])
mask_green = cv.inRange(img_hsv, lower_green, upper_green)
#cv.imshow("mask green", mask_green)

#masking brown (burnt grass)
lower_brown = np.array([4, 15, 5])
upper_brown = np.array([30, 255,255])
mask_brown = cv.inRange(img_hsv, lower_brown, upper_brown)
#cv.imshow("mask brown", mask_brown)    

img[mask_green>0] = [253,255,128]
img[mask_brown>0] = [90,238,252]
#cv.imshow("modified img", img)                  

x=cv.bitwise_or(mask_red,mask_brown) 
#cv.imshow("x",x)

blur = cv.GaussianBlur(mask_blue, (11, 11), 0)
cv.imshow('blur', blur)

#blurring
#blur = cv.blur(x, (5,6))

#Laplacian 
#lap = cv.Laplacian(mask_blue, cv.CV_64F)
#lap = np.uint8(np.absolute(lap))


canny = cv.Canny(blur, 30, 150,3)
cv.imshow('canny edges', canny)

contours, hierarchies= cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contours)} contour(s) found!')

                

cv.waitKey(0)

cv.destroyAllWindows()

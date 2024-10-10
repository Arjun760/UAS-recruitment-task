#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np

def contourfig(source):
    i=0
    contours, hierarchy = cv.findContours(source, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
     approx = cv.approxPolyDP(cnt,0.01*cv.arcLength(cnt,True),True)
     if len(approx)==3:
       i=i+1
    return i

img = cv.imread('/Users/arjunmalik/Downloads/uas takimages/1.png')
cv.imshow("original image", img)

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
cv.imshow("modified img", img)                  

#blur = cv.GaussianBlur(mask_blue, (5, 5), 0)
#cv.imshow('blur', blur)

#blurring
#blur = cv.blur(x, (5,6))

#Laplacian 
#lap = cv.Laplacian(mask_blue, cv.CV_64F)
#lap = np.uint8(np.absolute(lap))


#canny = cv.Canny(x, 30, 150,3)
#cv.imshow('canny edges', canny)

#contours, hierarchies= cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
#print(f'{len(contours)} contour(s) found!')

p=cv.bitwise_or(mask_red,mask_brown) #red house in green
tRG= contourfig(p)
#cv.imshow("red in green",p)

q=  cv.bitwise_or(mask_red, mask_green) #red house in brown
tRB= contourfig(q)
#cv.imshow("red in brown",q)

r= cv.bitwise_or(mask_blue,mask_brown) #blue houses in green
tBG= contourfig(r)
#cv.imshow("blue in green",r)

s= cv.bitwise_or(mask_blue,mask_green) #blue houses in brown
tBB= contourfig(s)
#cv.imshow("blue in brown", s)

a= [tRB+tBB, tRG+tBG] #total houses in different grass
b= [(tRB*1)+(tBB*2) , (tRG*1)+(tBG*2)] #total priority
c= ((tRB*1)+(tBB*2))/((tRG*1)+(tBG*2))

print('>>(house in burnt, houses in unburnt) = ', a)      
print('>>(Total priority on burnt grass (Pb), Total priority on unburnt grass (Pg) =', b)          
print('>>Rescue ratio of priority =', c)

cv.waitKey(0)

cv.destroyAllWindows()

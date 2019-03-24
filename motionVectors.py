#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:28:53 2019

@author: suchit
"""

import cv2
import numpy as np
from scipy import misc
import math


sample1 = np.zeros((512,512))
sample2 = np.zeros((512,512))
sample3 = np.zeros((512,512))

def bounding_boxes(present_frame):
    global x,y,obj,we,he
    _,contours,hierarchy = cv2.findContours(present_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
            xe,ye,we,he = cv2.boundingRect(cnt)
            if xe > 0:
                    if ye > 0:
                            if he > 30:
                                    if we > 30:
                                            
                                            x = (xe+he)/2
                                            y = (ye+we)/2
                                            
                                            
            #collecting object
            obj = np.zeros((he,we))
            for i in range(he):
                for j in range(we):
                    if(present_frame[i+ye,j+xe]!=0):
                        obj[i,j]=present_frame[i+ye,j+xe]
                                            
    return y,x
                                            


# Finding bounding contours for two input images
frame1=np.array(cv2.cvtColor((misc.imread("past.png")),cv2.COLOR_BGR2GRAY))
x1,y1=bounding_boxes(frame1)
 
frame2=np.array(cv2.cvtColor((misc.imread("present.png")),cv2.COLOR_BGR2GRAY))
x2,y2=bounding_boxes(frame2)


#motion vectors
slope = (x2-x1)/(y2-y1)
angle = math.atan(slope)
angle_deg=math.degrees(angle)
length = math.sqrt((y2-y1)**2+(x2-x1)**2)
frame_speed = length/33.36;

#extrapolation
if(angle_deg<=90 and angle_deg>=0):
    new_x1 = (x2+frame_speed * math.sin(angle)) % 512
    new_y1 = (y2+frame_speed * math.cos(angle))%512

    new_x2 = (x2+frame_speed * math.sin(angle)*33.36)%512
    new_y2 = (y2+frame_speed * math.cos(angle)*33.36)%512

    new_x3 = (x2+frame_speed * math.sin(angle)*100)%512
    new_y3 = (y2+frame_speed * math.cos(angle)*100)%512
elif(angle_deg>90 and angle_deg<=180):
    new_x1 = (x2+frame_speed * math.sin(angle))%512
    new_y1 = (y2-frame_speed * math.cos(angle))%512

    new_x2 = (x2+frame_speed * math.sin(angle)*33.36)%512
    new_y2 = (y2-frame_speed * math.cos(angle)*33.36)%512

    new_x3 = (x2+frame_speed * math.sin(angle)*1000)%512
    new_y3 = (y2-frame_speed * math.cos(angle)*1000)%512
elif(angle_deg>180 and angle_deg<=270):
    new_x1 = (x2-frame_speed * math.sin(angle))%512
    new_y1 = (y2-frame_speed * math.cos(angle))%512

    new_x2 = (x2-frame_speed * math.sin(angle)*33.36)%512
    new_y2 = (y2-frame_speed * math.cos(angle)*33.36)%512

    new_x3 = (x2-frame_speed * math.sin(angle)*1000)%512
    new_y3 = (y2-frame_speed * math.cos(angle)*1000)%512
elif(angle_deg>270 and angle_deg<=359):
    new_x1 = (x2-frame_speed * math.sin(angle))%512
    new_y1 = (y2+frame_speed * math.cos(angle))%512

    new_x2 = (x2-frame_speed * math.sin(angle)*33.36)%512
    new_y2 = (y2+frame_speed * math.cos(angle)*33.36)%512

    new_x3 = (x2-frame_speed * math.sin(angle)*1000)%512
    new_y3 = (y2+frame_speed * math.cos(angle)*1000)%512



#new boundary box middle

sample1[int(new_x1),int(new_y1)]=255    
sample2[int(new_x2),int(new_y2)]=255
sample3[int(new_x3),int(new_y3)]=255 

k1 = int(new_x1-he/2)
l1 = int(new_y1-we/2)
print(k1,l1)

for i in range(he):
    for j in range(we):
        sample1[k1,l1]=obj[i,j]
        l1=l1+1
    l1=int(new_y1-we/2)
    k1=k1+1
    
k1 = int(new_x2-he/2)
l1 = int(new_y2-we/2)
print(k1,l1)

for i in range(he):
    for j in range(we):
        sample2[k1,l1]=obj[i,j]
        l1=l1+1
    l1=int(new_y2-we/2)
    k1=k1+1
    
k1 = int(new_x3-he/2)
l1 = int(new_y3-we/2)
print(k1,l1)

for i in range(he):
    for j in range(we):
        sample3[k1,l1]=obj[i,j]
        l1=l1+1
    l1=int(new_y3-we/2)
    k1=k1+1
 

#output images        
cv2.imwrite('out1.png',sample1)
cv2.imwrite('out2.png',sample2)
cv2.imwrite('out3.png',sample3)

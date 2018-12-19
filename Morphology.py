#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 23:56:28 2018

@author: varshath
"""

import numpy as np
import cv2



def erosion(kernel,matrix):
    res=np.zeros((matrix.shape[0],matrix.shape[1]))
    for i in range(matrix.shape[0]-kernel.shape[0]+1):
        for j in range(matrix.shape[1]-kernel.shape[1]+1):
            if compareForErosion(i,j,kernel,matrix):
                res[i+1][j+1]=255
    return res

def compareForErosion(x,y,kernel,matrix):
    for i in range(kernel.shape[0]):
        for j in range(kernel.shape[1]):
            if kernel[i,j]!=matrix[x+i,y+j]:
                return False
    return True

def compareForDilation(x,y,kernel,matrix):
    for i in range(kernel.shape[0]):
        for j in range(kernel.shape[1]):
            if kernel[i,j]==255 and matrix[x+i,y+j]==255:
                return True
    return False


def dilation(kernel,matrix):
    res=np.zeros((matrix.shape[0],matrix.shape[1]))
    for i in range(matrix.shape[0]-kernel.shape[0]+1):
        for j in range(matrix.shape[1]-kernel.shape[1]+1):
            if compareForDilation(i,j,kernel,matrix):
                res[i+1][j+1]=255
    return res


def opening(kernel,matrix):
    res=erosion(kernel,matrix)
    res=dilation(kernel,res)
    return res


def closing(kernel,matrix):
    res=dilation(kernel,matrix)
    res=erosion(kernel,res)
    return res

def removeNoiseMethodA(kernel,matrix):
    res=opening(kernel,matrix)
    res=closing(kernel,res)
    return res
def removeNoiseMethodB(kernel,matrix):
    res=closing(kernel,matrix)
    res=opening(kernel,res)
    return res



def normalise(img):
    return (img - np.min(img)) / (np.max(img) - np.min(img))*255

img_matrix = cv2.imread("original_imgs/noise.jpg",0)
kernel=np.asmatrix([[255,255,255],[255,255,255],[255,255,255]])


resulting_image_a=removeNoiseMethodA(kernel,img_matrix)
resulting_image_b=removeNoiseMethodB(kernel,img_matrix)

cv2.imwrite('res_noise1.jpg',resulting_image_a)
cv2.imwrite('res_noise2.jpg',resulting_image_b)




eroded_a=erosion(kernel,resulting_image_a)
eroded_b=erosion(kernel,resulting_image_b)

#NOTE: Here Below we are subtracting the resulting image with eroded image to give us the boundary.
cv2.imwrite('res_bound1.jpg',resulting_image_a-eroded_a)
cv2.imwrite('res_bound2.jpg',resulting_image_b-eroded_b)


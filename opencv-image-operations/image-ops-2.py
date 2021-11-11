import numpy as np
import cv2 as cv

img = cv.imread('frame1.jpg')

px = img[100,100]
print( px )

# accessing only blue pixel
blue = img[100,100,0]
print(blue)

print(img.shape)
print(img.size)
print(img.dtype)


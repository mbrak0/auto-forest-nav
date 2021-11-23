import cv2
import numpy as np
import glob
import os
import sys
import time

imagename = "/home/matt-ip/Desktop/ForestGenerator-1.2/frames/frame--depth-0.jpg"
#print(imagename)
img = cv2.imread(imagename, 0) # 0 params, for grey image; 600x800 image
rows, cols = img.shape[:2]  # image height and width
#print(img)  # all image pixels value in array
#print(img[10, 10])  # one pixel value in 10,10 coordinate

y1 = 0
x1 = 0
M = rows//20 # image height divided by 20
N = cols//20 # image width divided by 20

obstacle = False

for y in range(0,rows,M):
	for x in range(0,cols,N):
		y1 = y + M
		x1 = x + N
		tile = img[y:y+M, x:x+N]

		tile_img_name = "/home/matt-ip/Desktop/auto-forest-nav/img-tiles/img_" + str(x) + '_' + str(y) + ".jpg"

		##tile = cv2.bitwise_not(tile)
		#cv2.rectangle(img, (x,y), (x1,y1), (0,255,0))
		cv2.imwrite(tile_img_name, tile)

		#tile = cv2.bitwise_not(tile)
		##cv2.imwrite(tile_img_name, tile)

		##tile_img = cv2.imread(tile_img_name, 0)
		"""
		if cv2.countNonZero(tile_img) == 0:
			print("test")
			obstacle = True
			break
		"""

		if np.mean(tile) >= 245:
			print("OBSTACLE DETECTED")
			obstacle = True
			break
	else:
		continue
	break

cv2.imwrite("/home/matt-ip/Desktop/auto-forest-nav/img-tiles/img-tiles.jpg", img)

if obstacle == False:
	print("w")
else:
	print("l")

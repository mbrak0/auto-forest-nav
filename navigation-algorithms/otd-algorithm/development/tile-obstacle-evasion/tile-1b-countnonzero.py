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

#for y in range(0,rows,M): # whole image in tiles
for y in range(int(0.6*rows),rows,M): # bottom 60% of image in tiles
	#for x in range(0,cols,N):
	for x in range(int(cols*0.125),int(cols*0.875),N):
		y1 = y + M
		x1 = x + N
		tile = img[y:y+M, x:x+N]

		tile_img_name = "/home/matt-ip/Desktop/auto-forest-nav/img-tiles/img_" + str(x) + '_' + str(y) + ".jpg"

		cv2.rectangle(img, (x,y), (x1,y1), (0,255,0))
		#cv2.imwrite(tile_img_name, tile)

		##tile_img = cv2.imread(tile_img_name, 0)

		thresh = cv2.threshold(tile, 230, 255, cv2.THRESH_BINARY)[1]
		
		pixels = cv2.countNonZero(thresh)

		if pixels == (M * N):
			#print("OBSTACLE DETECTED")
			obstacle = True
			#break
	
	#else:
		#continue
	#break

cv2.imwrite("/home/matt-ip/Desktop/auto-forest-nav/img-tiles/img-tiles.jpg", img)

if obstacle == False:
	print("w")
else:
	print("l")

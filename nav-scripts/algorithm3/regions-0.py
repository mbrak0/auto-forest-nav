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

"""
y1 = 0
x1 = 0
M = rows//20 # image height divided by 20
N = cols//20 # image width divided by 20

obstacle = False

#for y in range(0,rows,M): # whole image in tiles
for y in range(int(0.55*rows),rows,M): # bottom 60% of image in tiles
	#for x in range(0,cols,N):
	for x in range(int(cols*0.15),int(cols*0.85),N):
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

cv2.imwrite("/home/matt-ip/Desktop/auto-forest-nav/img-tiles/img-tiles-45_15_85.jpg", img)

if obstacle == False:
	print("w")
else:
	print("l")
"""

left_reg = img[0:rows, 0:266]
#cv2.imwrite("/home/matt-ip/Desktop/auto-forest-nav/img-tiles/img-left.jpg", left_reg)
#print(left_reg)

right_reg = img[0:rows, 534:cols]
#cv2.imwrite("/home/matt-ip/Desktop/auto-forest-nav/img-tiles/img-right.jpg", right_reg)

mid_reg = img[0:rows, 266:534]
#cv2.imwrite("/home/matt-ip/Desktop/auto-forest-nav/img-tiles/img-mid.jpg", mid_reg)

left_mean, right_mean, mid_mean = np.mean(left_reg), np.mean(right_reg), np.mean(mid_reg)

reg_mean_arr = [left_mean, mid_mean, right_mean]

least_obs = np.argmin(reg_mean_arr)

print("Left: " + str(left_mean) + ", Mid: " + str(mid_mean) + ", Right: " + str(right_mean))
print(least_obs)

#if least_obs == 0:

weighted_mat_lr = np.zeros((rows,266))

for x in range(0,rows):
	for y in range(0,266):
		weighted_mat_lr[x][y] = x+1

weighted_mat_mid = np.zeros((rows,268))

for x in range(0,rows):
	for y in range(0,268):
		weighted_mat_mid[x][y] = x+1

print(weighted_mat_lr)
print(weighted_mat_lr.shape)
print(left_reg.shape)

left_w_avg = np.average(left_reg, weights = weighted_mat_lr)
right_w_avg = np.average(right_reg, weights = weighted_mat_lr)
mid_w_avg = np.average(mid_reg, weights = weighted_mat_mid)

print(left_w_avg)
print(right_w_avg)
print(mid_w_avg)

reg_w_avg_arr = [left_w_avg, mid_w_avg, right_w_avg]

least_obs_w = np.argmin(reg_w_avg_arr)

print("Left: " + str(left_w_avg) + ", Mid: " + str(mid_w_avg) + ", Right: " + str(right_w_avg))
print(least_obs_w)
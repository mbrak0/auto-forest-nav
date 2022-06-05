import cv2
import numpy as np
import glob
import os
import sys
import time
from scipy.stats import norm

def weightedMat(rows, columns, weights):
	weighted_mat = np.zeros((rows,columns))
	for x in range(0,rows):
		for y in range(0,columns):
			weighted_mat[x][y] = weights[x]
	return weighted_mat

#imagename = "/home/matt-ip/Desktop/temp/frames/frame--depth-0.jpg"
#imagename = "/home/matt-ip/Desktop/logs/algorithm2/density-real/dense/seed2/frames/frame--depth-546.jpg"
#imagename = "/home/matt-ip/Desktop/logs/algorithm2/density-real/dense/seed2/frames/frame--depth-576.jpg"
#imagename = "/home/matt-ip/Desktop/logs/algorithm2/no-obs-det/default/seed3/frames/frame--depth-2040.jpg"
imagename = "/home/matt-ip/Desktop/logs/collision-evaded0.jpg"
#print(imagename)
img = cv2.imread(imagename, 0) # 0 params, for grey image; 600x800 image
rows, cols = img.shape[:2]  # image height and width
#print(img)  # all image pixels value in array
#print(img[10, 10])  # one pixel value in 10,10 coordinate

print(cols)

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

weight_scale_arr = ["normal distribution", "linear", "logarithmic"]
weight_scale = weight_scale_arr[0]

row_indices = np.arange(1,601,1)
weights = []

if weight_scale == "normal distribution":
	pdf = norm.pdf(row_indices, loc=300.5, scale=60)
	for k in pdf:
		weights.append(k/max(pdf))

elif weight_scale == "linear":
	for l in row_indices:
		weights.append(l/600)

elif weight_scale == "logarithmic":
	base = 2
	for m in row_indices:
		weights.append((base**(int(m)-1))/(base**599))
	
weighted_mat_lr = weightedMat(600, 266, weights)
weighted_mat_mid = weightedMat(600, 268, weights)
weighted_mat_half = weightedMat(600, 400, weights)

"""
weighted_mat_lr = np.zeros((rows,266))

for x in range(0,rows):
	for y in range(0,266):
		weighted_mat_lr[x][y] = x+1

weighted_mat_mid = np.zeros((rows,268))

for x in range(0,rows):
	for y in range(0,268):
		weighted_mat_mid[x][y] = x+1
"""

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

#cv2.rectangle(img, (0,0), (265,0), (0,255,0))
cv2.rectangle(img, (265,0), (534,800), (0,255,0))
#cv2.rectangle(img, (535,800), (601,800), (0,255,0))
#cv2.show(img)
#cv2.imwrite("/home/matt-ip/Desktop/auto-forest-nav/img-tiles/reg-nav-no-obs-det-collision.jpg", img)

cv2.imwrite("/home/matt-ip/Desktop/logs/collision-evaded.jpg", img)

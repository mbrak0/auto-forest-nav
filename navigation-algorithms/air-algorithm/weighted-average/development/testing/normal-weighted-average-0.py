import cv2
import numpy as np
import glob
import os
import sys
import time
import numpy as np
import inotify.adapters

from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sb

from matplotlib.pyplot import figure

def weightedMatLin(rows, columns):
	weighted_mat = np.zeros((rows,columns))
	for x in range(0,rows):
		for y in range(0,columns):
			weighted_mat[x][y] = x+1
	return weighted_mat

def weightedMatLog(rows, columns):
	weighted_mat = np.zeros((rows,columns))
	for x in range(0,rows):
		for y in range(0,columns):
			weighted_mat[x][y] = 2**x
	return weighted_mat

def weightedMatNorm(rows, columns, weights):
	weighted_mat = np.zeros((rows,columns))
	for x in range(0,rows):
		for y in range(0,columns):
			weighted_mat[x][y] = weights[x]
	return weighted_mat

"""
sb.set_style('whitegrid')
sb.lineplot(data, pdf , color = 'black')
plt.xlabel('Heights')
plt.ylabel('Probability Density')
plt.show()
"""

#path = '/home/matt-ip/Desktop/temp/frames/frame--depth-34.jpg'
path = '/home/matt-ip/Desktop/auto-forest-nav/report-images/three-regions1.jpg'
img = cv2.imread(path, 0) # 0 params, for grey image
rows, cols = img.shape[:2]  # image height and width

left_reg = img[0:rows, 0:int(round((1/3)*cols)-1)]
right_reg = img[0:rows, int(round((2/3)*cols)+1):cols]
mid_reg = img[0:rows, int(round((1/3)*cols)-1):int(round((2/3)*cols)+1)]

left_mean, right_mean, mid_mean = np.mean(left_reg), np.mean(right_reg), np.mean(mid_reg)
reg_mean_arr = [left_mean, mid_mean, right_mean]

least_obs = np.argmax(reg_mean_arr)
#least_obs_arr.append(least_obs)
most_obs = np.argmin(reg_mean_arr)

#weighted_mat_lr = weightedMatLog(rows, 266)
#weighted_mat_mid = weightedMatLog(rows, 268)

"""
weighted_mat_lr = np.zeros((rows,266))
for x in range(0,rows):
	for y in range(0,266):
		weighted_mat_lr[x][y] = 2**(x+1)

weighted_mat_mid = np.zeros((rows,268))
for x in range(0,rows):
	for y in range(0,268):
		weighted_mat_mid[x][y] = x+1
"""

columns = 266

row_indices = np.arange(1,601,1)
#print(data)
pdf = norm.pdf(row_indices, loc=300.5, scale=60)
#pdf = norm.pdf(row_indices, loc=200, scale=60) #shifted
#print(pdf[298], pdf[299], pdf[300], pdf[301])
#print(max(pdf))



weights = []

for i in pdf:
	weights.append(i/max(pdf))

figure(figsize=(10, 6), dpi=80)
plt.plot(row_indices, weights)
#plt.plot(240.5,np.arange(0,1))
plt.xlabel("Data Points")
plt.ylabel("Probability Density")
#plt.grid()

#plt.show()

#print(max(weights))
"""
weighted_mat = np.zeros((600,columns))
for x in range(0,600):
	for y in range(0,columns):
		weighted_mat[x][y] = weights[x]
"""
weighted_mat_lr = weightedMatNorm(600, 266, weights)
weighted_mat_mid = weightedMatNorm(600, 268, weights)

#print(weighted_mat_mid)

left_w_avg = np.average(left_reg, weights = weighted_mat_lr)
right_w_avg = np.average(right_reg, weights = weighted_mat_lr)
mid_w_avg = np.average(mid_reg, weights = weighted_mat_mid)

reg_w_avg_arr = [left_w_avg, mid_w_avg, right_w_avg]
least_obs_w = np.argmax(reg_w_avg_arr)
#least_obs_arr.append(least_obs_w)
most_obs_w = np.argmax(reg_w_avg_arr)


left_half = img[0:rows, 0:int(0.5*cols)]
right_half = img[0:rows, int(0.5*cols):cols]

left_half_mean, right_half_mean = np.mean(left_half), np.mean(right_half)

weighted_mat_half = weightedMatLog(rows, 400)


weighted_mat_half = np.zeros((rows,400))
for x in range(0,rows):
	for y in range(0,400):
		weighted_mat_half[x][y] = x+1


left_half_w_avg = np.average(left_half, weights = weighted_mat_half)
right_half_w_avg = np.average(right_half, weights = weighted_mat_half)

#print("Left region shape = ", left_reg.shape, ", Mid region shape = ", mid_reg.shape, ", Right region shape = ", right_reg.shape)
print("Left region = ", left_w_avg, ", Mid region = ", mid_w_avg, ", Right region = ", right_w_avg)
#print("Left half = ", left_half_w_avg, ", Right half = ", right_half_w_avg)
#print(weighted_mat_lr.shape)
#print(weighted_mat_mid.shape)

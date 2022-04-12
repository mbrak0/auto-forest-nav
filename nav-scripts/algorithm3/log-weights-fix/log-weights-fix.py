import numpy as np
from scipy.stats import norm

def weightedMat(rows, columns, weights):
	weighted_mat = np.zeros((rows,columns))
	for x in range(0,rows):
		for y in range(0,columns):
			weighted_mat[x][y] = weights[x]
	return weighted_mat

weight_scale_arr = ["normal distribution", "linear", "logarithmic"]
weight_scale = weight_scale_arr[2]

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
	base = 1.05
	for m in row_indices:
		weights.append((base**(int(m)-1))/(base**599))
        #weights.append((2**(int(m)-1)))
	
weighted_mat_lr = weightedMat(600, 266, weights)
weighted_mat_mid = weightedMat(600, 268, weights)
weighted_mat_half = weightedMat(600, 400, weights)

print(weights)
#print(np.argmax(weights))
#print(2**64)
#print(2**int(row_indices[63]))
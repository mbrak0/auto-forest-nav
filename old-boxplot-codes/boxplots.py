import matplotlib.pyplot as plt
import numpy as np
import os

def logNum(x):
    return(x[7:9])

path1 = '/home/matt-ip/Desktop/logs/New2/Density/sparse10_90/stats/'
list_of_files1 = os.listdir(path1)
list_of_files1 = sorted(list_of_files1, key = logNum)
#print(list_of_files1)

num_moves_1_arr = []
euc_dis_1_arr = []
wobble_1_arr = []

for file in list_of_files1:
    
    file_path1 = path1 + file
    f1 = open(file_path1, "r")
    stats1 = f1.readlines()
    
    num_moves1 = int((stats1[16].split())[4])
    num_forward1 = int((stats1[17].split())[5])
    num_right1 = int((stats1[18].split())[5])
    num_left1 = int((stats1[19].split())[5])

    euc_dis1 = (7/30) * num_forward1
    wobble1 = (num_right1 + num_left1) / num_moves1
    
    num_moves_1_arr.append(num_moves1)
    euc_dis_1_arr.append(euc_dis1)
    wobble_1_arr.append(wobble1)

f1.close()

path2 = '/home/matt-ip/Desktop/logs/NewObs/Density/sparse/3regions2/stats/'
list_of_files2 = os.listdir(path2)
list_of_files2 = sorted(list_of_files2, key = logNum)

num_moves_2_arr = []
euc_dis_2_arr = []
wobble_2_arr = []

for file in list_of_files2:
    
    file_path2 = path2 + file
    f2 = open(file_path2, "r")
    stats2 = f2.readlines()
    
    num_moves2 = int((stats2[16].split())[4])
    num_forward2 = int((stats2[17].split())[5])
    num_right2 = int((stats2[18].split())[5])
    num_left2 = int((stats2[19].split())[5])

    euc_dis2 = (7/30) * num_forward2
    wobble2 = (num_right2 + num_left2) / num_moves2
    
    num_moves_2_arr.append(num_moves2)
    euc_dis_2_arr.append(euc_dis2)
    wobble_2_arr.append(wobble2)

f2.close()

moves_data = [num_moves_1_arr, num_moves_2_arr]
euc_dis_data = [euc_dis_1_arr, euc_dis_2_arr]
wobble_data = [wobble_1_arr, wobble_2_arr]

#print(moves_data)

fig = plt.figure(figsize=(10,7))
ax = fig.add_axes([0.1,0.1,0.8,0.8])

bp = ax.boxplot(moves_data)
#bp = ax.boxplot(euc_dis_data)
#bp = ax.boxplot(wobble_data)
plt.show()
import matplotlib.pyplot as plt
import numpy as np
import os

seed_num = list(range(1,6))
#print(seed_num)

alg_select = [1,2]

moves_num_arr = []
euc_dis_arr = []
wobble_rate_arr = []
col_arr = []

"""
path1 = "/home/matt-ip/Desktop/logs/algorithm1/density/sparse/seed1/logfile.txt"

f1 = open(path1, "r")
log1 = f1.readlines()
f1.close()

num_of_moves = log1[16].split()[4]
euc_dis = log1[21].split()[4]
wobble_rate = log1[22].split()[3]

moves_num_arr.append(num_of_moves)
euc_dis_arr.append(euc_dis)
wobble_rate_arr.append(wobble_rate)
"""

for i in alg_select:
    for j in seed_num:
        path = "/home/matt-ip/Desktop/logs/algorithm" + str(i) + "/density/sparse/seed" + str(j) + "/logfile.txt"
        #print(path)

        f = open(path, "r")
        log = f.readlines()
        f.close()

        num_of_moves = float(log[16].split()[4])
        euc_dis = float(log[21].split()[4])
        wobble_rate = float(log[22].split()[3])
        num_of_collisions = float(log[23].split()[4])

        moves_num_arr.append(num_of_moves)
        euc_dis_arr.append(euc_dis)
        wobble_rate_arr.append(wobble_rate)
        col_arr.append(num_of_collisions)

#print(moves_num_arr)
#print(euc_dis_arr)
#print(wobble_rate_arr)
#print(col_arr)

moves_data = [moves_num_arr[0:5], moves_num_arr[5:10]]
euc_dis_data = [euc_dis_arr[0:5], euc_dis_arr[5:10]]
wobble_data = [wobble_rate_arr[0:5], wobble_rate_arr[5:10]]
collision_data = [col_arr[0:5], col_arr[5:10]]

#print(moves_num_arr[0:5])
#print(moves_data)

fig = plt.figure(figsize=(10,7))
ax = fig.add_axes([0.1,0.1,0.8,0.8])

#bp = ax.boxplot(moves_data)
#plt.ylabel("Number of Moves")

#bp = ax.boxplot(euc_dis_data)
#plt.ylabel("Euclidean Distance Travelled (m)")

#bp = ax.boxplot(wobble_data)
#plt.ylabel("Wobble Rate")

#bp = ax.boxplot(collision_data)
#plt.ylabel("Number of Collisions")

plt.xticks([1, 2], ["Algorithm 1", "Algorithm 2"])

boxplot_label = "collisions_1v2"
fig.savefig("/home/matt-ip/Desktop/logs/Boxplots/" + str(boxplot_label))

plt.show()

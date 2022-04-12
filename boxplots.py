import matplotlib.pyplot as plt
import numpy as np
import os
from tabulate import tabulate

seed_num = [1,2,3,5,6,7,8,9,10,11]
#seed_num = [1,2,3,5,6]
#print(seed_num)

#alg_select = [1,2,3]
alg_select = [3]

#sim_param = "density"
#sim_param = "goal-correction"
sim_param_select = ["density-no-obs-det","density-linear","density-log2"]

#sim_param_variant_list  = ["sparse", "default", "dense"]
sim_param_variant_list  = ["default"]
#sim_param_variant_list  = ["goal-corr20","goal-corr40"]
#sim_param_variant_list  = ["density","density-no-obs-det"]

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
    for sim_param in sim_param_select:
        for j in sim_param_variant_list:
            for k in seed_num:
                path = "/home/matt-ip/Desktop/logs/algorithm" + str(i) + "/" + str(sim_param) + "/" + str(j) + "/seed" + str(k) + "/logfile.txt"
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

moves_data = [moves_num_arr[0:len(seed_num)], moves_num_arr[len(seed_num):2*len(seed_num)], moves_num_arr[2*len(seed_num):3*len(seed_num)]]
euc_dis_data = [euc_dis_arr[0:len(seed_num)], euc_dis_arr[len(seed_num):2*len(seed_num)], euc_dis_arr[2*len(seed_num):3*len(seed_num)]]
wobble_data = [wobble_rate_arr[0:len(seed_num)], wobble_rate_arr[len(seed_num):2*len(seed_num)], wobble_rate_arr[2*len(seed_num):3*len(seed_num)]]
collision_data = [col_arr[0:len(seed_num)], col_arr[len(seed_num):2*len(seed_num)], col_arr[2*len(seed_num):3*len(seed_num)]]

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

metric = "Moves"
if metric == "Moves":
    data = moves_data
    plt.ylabel("Number of Moves")
    #plt.yticks(list(range(0,11000,1000)))
    #plt.yticks(list(range(0,11000,500)))
    #plt.ylim(0,10500)
    #plt.ylim(500,3750)
    #plt.ylim(500,4500)
    #plt.yticks(list(range(650,1450,50)))
    #plt.ylim(650,1400)
    #plt.yticks(list(range(800,2500,100)))
    #plt.ylim(800,2400)
elif metric == "EuclideanDistance":
    data = euc_dis_data
    plt.ylabel("Euclidean Distance Travelled (m)")
    #plt.yticks(list(range(120,300,10)))
    #plt.ylim(120,270)
    #plt.yticks(list(range(120,200,5)))
    #plt.ylim(125,175)
    #plt.yticks(list(range(120,200,5)))
    #plt.yticks(list(range(125,195,10)))
    #plt.ylim(125,195)
    #plt.yticks([127,127.5,128,128.5,129,129.5,130,130.5,131,131.5,132,132.5,133,133.5,134])
    #plt.ylim(127,134)
    #plt.yticks([127.5,130,132.5,135,137.5,140,142.5,145,147.5,150])
    #plt.yticks([127,129,131,133,135,137,139,141,143,145,147,149])
    #plt.ylim(127.5,150)
    #plt.ylim(127,149)
    #plt.yticks(list(range(120,280,10)))
    #plt.ylim(120,270)
elif metric == "WobbleRate":
    data = wobble_data
    plt.ylabel("Wobble Rate")
    #plt.yticks([0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95])
    #plt.ylim(0.15,0.95)
    #plt.yticks([0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80])
    #plt.ylim(0.2,0.8)
    #plt.yticks([0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85])
    #plt.ylim(0.25,0.85)
    #plt.ylim(0.35,0.75)
    plt.ylim(0.3,0.9)
elif metric == "Collisions":
    data = collision_data
    plt.ylabel("Number of Collisions")
    #plt.yticks([0,0.5,1.0,1.5,2.0])
    #plt.yticks([0,1.0,2.0,3.0])

table = [[]]
table_headings = ["Density","Seed 1","Seed 2","Seed 3","Seed 5","Seed 6","Seed 7","Seed 8","Seed 9","Seed 10","Seed 11","Average"]

entry1 = ["1"]
for i in data[0]:
    entry1.append(i)
entry1.append(np.mean(data[0]))

entry2 = ["2"]
for j in data[1]:
    entry2.append(j)
entry2.append(np.mean(data[1]))

entry3 = ["3"]
for k in data[2]:
    entry3.append(k)
entry3.append(np.mean(data[2]))

table.append(table_headings)
table.append(entry1)
table.append(entry2)
table.append(entry3)

print(tabulate(table))

#print(min(data[0]), min(data[1]), min(data[2]))
#print(max(data[0]), max(data[1]), max(data[2]))

bp = ax.boxplot(data)

axes = plt.gca()
axes.yaxis.grid()

#plt.xticks([1, 2, 3], ["Algorithm 1", "Algorithm 2", "Algorithm 3"])
#plt.xticks([1, 2, 3], ["Sparse", "Default", "Dense"])
#plt.xticks([1, 2, 3], ["20", "40", "Algorithm 3"])
#plt.xticks([1, 2], ["Obs 40", "Obs 50"])
plt.xticks([1, 2, 3], ["Normal Dist", "Linear", "Log Base 2"])

boxplot_label = "Dense_Algorithm123_" + str(metric)

#fig.savefig("/home/matt-ip/Desktop/logs/Boxplots/" + str(boxplot_label) + ".png", dpi=80)

plt.show()

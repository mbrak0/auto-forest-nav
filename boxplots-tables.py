import matplotlib.pyplot as plt
import numpy as np
import os
from tabulate import tabulate
from scipy import stats

seed_num = [1,2,3,5,6,7,8,9,10,11]
#seed_num = [1,2,3,10,11]
#print(seed_num)

#alg_select = [1,2,3]
alg_select = [3]

#sim_param_select = ["density-real","tiles-obstacle-detection-31875"]
#sim_param_select = ["density-real","goal-correct-40","goal-correct-60"]
#sim_param_select = ["tiles-obstacle-detection-19125","density-real","tiles-obstacle-detection-31875"]
#sim_param_select = ["density-real","linear","log-base-1-01"]
#sim_param_select = ["density-real","obs-det-50","obs-det-60"]
#sim_param_select = ["no-reg-nav-halt","density-real","obs-det-50"]
#sim_param_select = ["no-obs-det","obs-det-40","density-real"]
#sim_param_select = ["no-obs-det-2","obs-det-40","density-real","obs-det-60"]
#sim_param_select = ["alg2-no-reg-nav-halt","no-obs-det-2","density-real"]
#sim_param_select = ["linear-2","log-base-1-001-2","no-obs-det-2"]
#sim_param_select = ["no-obs-det-2","no-obs-det-2-gc-40"]
#sim_param_select = ["no-obs-det","density-real","obs-det-50","obs-det-60"]
#sim_param_select = ["density-real","goal-correct-40"]
#sim_param_select = ["alg1-final","no-obs-det-2","density-real"]
#sim_param_select = ["density-real","goal-correct-40","linear-2"]
sim_param_select = ["alg1-final","no-obs-det-2","goal-correct-40"]

#sim_param_select = ["no-obs-det-2"]
#sim_param_variant_list  = ["sparse", "default", "dense"]
sim_param_variant_list  = ["dense"]
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

if len(sim_param_select) == 4:
    moves_data = [moves_num_arr[0:len(seed_num)], moves_num_arr[len(seed_num):2*len(seed_num)], moves_num_arr[2*len(seed_num):3*len(seed_num)], moves_num_arr[3*len(seed_num):4*len(seed_num)]]
    euc_dis_data = [euc_dis_arr[0:len(seed_num)], euc_dis_arr[len(seed_num):2*len(seed_num)], euc_dis_arr[2*len(seed_num):3*len(seed_num)], euc_dis_arr[3*len(seed_num):4*len(seed_num)]]
    wobble_data = [wobble_rate_arr[0:len(seed_num)], wobble_rate_arr[len(seed_num):2*len(seed_num)], wobble_rate_arr[2*len(seed_num):3*len(seed_num)], wobble_rate_arr[3*len(seed_num):4*len(seed_num)]]
    collision_data = [col_arr[0:len(seed_num)], col_arr[len(seed_num):2*len(seed_num)], col_arr[2*len(seed_num):3*len(seed_num)], col_arr[3*len(seed_num):4*len(seed_num)]]
elif len(sim_param_select) == 2:
    moves_data = [moves_num_arr[0:len(seed_num)], moves_num_arr[len(seed_num):2*len(seed_num)]]
    euc_dis_data = [euc_dis_arr[0:len(seed_num)], euc_dis_arr[len(seed_num):2*len(seed_num)]]
    wobble_data = [wobble_rate_arr[0:len(seed_num)], wobble_rate_arr[len(seed_num):2*len(seed_num)]]
    collision_data = [col_arr[0:len(seed_num)], col_arr[len(seed_num):2*len(seed_num)]]


#print(moves_num_arr[0:5])
#print(moves_data)

fig = plt.figure(figsize=(7.5,7))
#fig = plt.figure(figsize=(7.5,5))
ax = fig.add_axes([0.1,0.1,0.8,0.8])

#bp = ax.boxplot(moves_data)
#plt.ylabel("Number of Moves")

#bp = ax.boxplot(euc_dis_data)
#plt.ylabel("Euclidean Distance Travelled (m)")

#bp = ax.boxplot(wobble_data)
#plt.ylabel("Wobble Rate")

#bp = ax.boxplot(collision_data)
#plt.ylabel("Number of Collisions")

metric = "WobbleRate"
if metric == "Moves":
    data = moves_data
    plt.ylabel("Number of Moves")
    #plt.yticks(list(range(0,11000,1000)))
    #plt.yticks(list(range(0,11000,100)))
    #plt.ylim(0,10500)
    #plt.ylim(600,1500)
    #plt.ylim(500,4750)
    #plt.yticks(list(range(650,1450,50)))
    #plt.ylim(600,1500)
    #plt.yticks(list(range(800,2500,100)))
    #plt.ylim(700,2400)
    #plt.ylim(800,1400)
    #plt.yticks(list(range(500,6500,1000)))
    #plt.ylim(500,5000)
    #plt.ylim(900,2800)

elif metric == "EuclideanDistance":
    data = euc_dis_data
    plt.ylabel("Euclidean Distance Travelled (m)")
    #plt.yticks(list(range(120,300,10)))
    #plt.ylim(120,220)
    #plt.yticks(list(range(120,220,10)))
    #plt.yticks(list(range(120,200,5)))
    #plt.yticks(list(range(125,195,10)))
    #plt.ylim(125,170)
    #plt.yticks([127,127.5,128,128.5,129,129.5,130,130.5,131,131.5,132,132.5,133,133.5,134])
    #plt.ylim(127,134)
    #plt.yticks([127.5,130,132.5,135,137.5,140,142.5,145,147.5,150])
    #plt.yticks([126,128,130,132,134,136,138,140,142,144,146,148,150])
    #plt.ylim(127.5,150)
    #plt.ylim(127,149)
    #plt.yticks(list(range(120,280,10)))
    #plt.yticks([125,135,145,155,165,175,185,195])
    #plt.ylim(125,195)
    #plt.ylim(125,325)
    #plt.ylim(100,450)
    #plt.ylim(126,145)

elif metric == "WobbleRate":
    data = wobble_data
    plt.ylabel("Wobble Rate")
    #plt.yticks([0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95])
    #plt.ylim(0.15,0.95)
    #plt.yticks([0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80])
    #plt.ylim(0.2,0.8)
    plt.yticks([0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85])
    #plt.ylim(0.15,0.65)
    plt.ylim(0.375,0.825)
    #plt.ylim(0.3,0.75)

elif metric == "Collisions":
    data = collision_data
    plt.ylabel("Number of Collisions")
    #plt.yticks([0,0.5,1.0,1.5,2.0])
    #plt.yticks([0,1.0,2.0,3.0])


table = [[]]
table_headings = ["Density","Seed 1","Seed 2","Seed 3","Seed 5","Seed 6","Seed 7","Seed 8","Seed 9","Seed 10","Seed 11","Mean","Standard Deviation"]

entry1 = ["1"]
for i in data[0]:
    entry1.append("{:.2f}".format(i))
entry1.append("{:.2f}".format(np.mean(data[0])))
entry1.append("{:.4f}".format(np.std(data[0])))

if len(sim_param_select) >= 2:
    entry2 = ["2"]
    for j in data[1]:
        entry2.append("{:.2f}".format(j))
    entry2.append("{:.2f}".format(np.mean(data[1])))
    entry2.append("{:.4f}".format(np.std(data[1])))

if len(sim_param_select) >= 3:
    entry3 = ["3"]
    for k in data[2]:
        entry3.append("{:.2f}".format(k))
    entry3.append("{:.2f}".format(np.mean(data[2])))
    entry3.append("{:.4f}".format(np.std(data[2])))

if len(sim_param_select) == 4:
    entry4 = ["4"]
    for l in data[3]:
        entry3.append("{:.2f}".format(l))
    entry3.append("{:.2f}".format(np.mean(data[3])))
    entry3.append("{:.4f}".format(np.std(data[3])))

table.append(table_headings)
table.append(entry1)
table.append(entry2)
if len(sim_param_select) == 3:
    table.append(entry3)
if len(sim_param_select) == 4:
    table.append(entry4)

print(tabulate(table))

#print(min(data[0]), min(data[1]), min(data[2]))
#print(max(data[0]), max(data[1]), max(data[2]))

print(stats.kruskal(data[0], data[1], data[2]))

bp = ax.boxplot(data)

axes = plt.gca()
axes.yaxis.grid()

#plt.xticks([1, 2, 3], ["Algorithm 1", "Algorithm 2", "Algorithm 3"])
#plt.xticks([1, 2, 3], ["Sparse", "Default", "Dense"])
#plt.xticks([1, 2, 3], ["Goal Correction 20", "Goal Correction 40", "Goal Correction 60"])
#plt.xticks([1, 2, 3, 4], ["No threshold", "Threshold 40", "Threshold 50", "Threshold 60"])
#plt.xticks([1, 2, 3], ["No threshold", "Threshold 40", "Threshold 50"])
#plt.xticks([1, 2, 3], ["Normal Dist", "Linear", "Log Base 2"])
#plt.xticks([1, 2, 3], ["Obstacle Detection 1.5m", "Obstacle Detection 2.0m", "Obstacle Detection 2.5m"])
plt.xticks([1, 2, 3], ["OTD", "AIR", "AIR-Plus"])
#plt.xticks([1, 2], ["Goal Correction 20", "Goal Correction 40"])

boxplot_label = "Alg0_High_" + str(metric)

#fig.savefig("/home/matt-ip/Desktop/logs/Boxplots/" + str(boxplot_label) + ".png", dpi=80)

#plt.show()

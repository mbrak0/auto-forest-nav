import matplotlib.pyplot as plt
import numpy as np
import os
import cv2

nav_log = []
x_pos_arr = []
z_pos_arr = []

#path = "/home/matt-ip/Desktop/logs/algorithm3/density/default/seed11/logfile.txt"
path = "/home/matt-ip/Desktop/logs/logfile.txt"

f = open(path, "r")
log = f.readlines()
f.close()

x_goal_pos = float(log[10].split()[3])
z_goal_pos = float(log[10].split()[5])

for i in range(27, len(log)-3):
    nav_log.append(log[i])

for j in nav_log:
    item = j.split("\t")
    pos = item[2]
    pos = pos.split(" ")
    x_pos, z_pos = float(pos[2]), float(pos[4])
    x_pos_arr.append(x_pos)
    z_pos_arr.append(z_pos)

fig, ax = plt.subplots(figsize=(8,8))
ax.scatter(x_pos_arr, z_pos_arr, s=2)

plt.plot(x_goal_pos, z_goal_pos, "gs")
plt.plot(x_pos_arr[0], z_pos_arr[0], "r^", x_pos_arr[-1], z_pos_arr[-1], "y^")

plt.xlabel("x")
plt.ylabel("z")
plt.yticks(np.arange(-50, 60, 10))
plt.xticks(np.arange(-50, 60, 10))
plt.xlim = ([-50,50])
plt.ylim = ([-50,50])
plt.grid()

plt.savefig("/home/matt-ip/Desktop/logs/algorithm3/density/sparse/seed3/traj-map3.png")
#plt.show()

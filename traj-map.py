import matplotlib.pyplot as plt
import numpy as np
import os
import cv2

nav_log = []
x_pos_arr = []
z_pos_arr = []

#path = "/home/matt-ip/Desktop/logs/Post-ProgressReport/FinalisedRegions/Density/default10_90/seed2/logfile.txt"
path = "/home/matt-ip/Desktop/logs/logfile.txt"

f = open(path, "r")
log = f.readlines()
#nav_log.append(log[26:len(log)-1])
#print(len(nav_log))
f.close()

x_goal_pos = float(log[10].split()[3])
z_goal_pos = float(log[10].split()[5])
#print(x_goal_pos, z_goal_pos)

for i in range(27, len(log)-3):
    nav_log.append(log[i])

#print(nav_log)

"""
item = nav_log[0].split("\t")
pos = item[2]
#print(item)
#print(pos)

pos = pos.split(" ")
#print(pos)

x_pos, z_pos = pos[2], pos[4]
print(x_pos, z_pos)

x_pos_arr.append(x_pos)
z_pos_arr.append(z_pos)

#print(x_pos_arr)
"""

for j in nav_log:
    item = j.split("\t")
    pos = item[2]
    #print(item)
    #print(pos)

    pos = pos.split(" ")
    #print(pos)

    x_pos, z_pos = float(pos[2]), float(pos[4])
    #print(x_pos, z_pos)

    x_pos_arr.append(x_pos)
    z_pos_arr.append(z_pos)

#print(z_pos_arr)

#img = plt.imread("/home/matt-ip/Desktop/auto-forest-nav/forest_background_crop.jpg")
fig, ax = plt.subplots(figsize=(8,8))
#fig, ax = plt.subplots()
#ax.imshow(img, extent=[-50, 50, -50, 50])
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

plt.savefig("/home/matt-ip/Desktop/logs/algorithm3/density/default/seed3-0point15/traj-map.png")
plt.show()

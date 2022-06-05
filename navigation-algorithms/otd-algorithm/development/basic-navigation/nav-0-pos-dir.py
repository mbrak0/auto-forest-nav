import cv2
import numpy as np
import glob
import os
import sys
import time

goal_x = float(25.0)
goal_z = float(25.0)

list_of_check = glob.glob('/home/matt-ip/Desktop/ForestGenerator-1.2/checkpoints/*')
latest_checkpoint = max(list_of_check, key=os.path.getctime)
#print(latest_checkpoint)

f = open(latest_checkpoint, "r")

#for i in range(30,32):
	#print(f.readlines()[i])

pos_direc = f.readlines()[29:37]
#print(pos_direc)

x_pos = float(str((pos_direc[1].split())[1]))
y_pos = float(str((pos_direc[2].split())[1]))
z_pos = float(str((pos_direc[3].split())[1]))

x_direc = float(str((pos_direc[5].split())[1]))
y_direc = float(str((pos_direc[6].split())[1]))
z_direc = float(str((pos_direc[7].split())[1]))

print("Position\t-\tx: " + str(x_pos) + "\ty: " + str(y_pos) + "\tz: " + str(z_pos))
print("Direction\t-\tx: " + str(x_direc) + "\ty: " + str(y_direc) + "\tz: " + str(z_direc))

"""
if (abs(x_pos) or abs(z_pos)) >= 50:
	print("OUT OF BOUNDS")
	print("l")
	print("w")
else:
	print("IN FOREST")
"""

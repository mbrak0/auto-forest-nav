import cv2
import numpy as np
import glob
import os
import sys
import time
import numpy as np
import inotify.adapters

f4 = open("/home/matt-ip/Desktop/logs/cmdline-output-log.txt", "r")
outputs = f4.readlines()
f4.close()

collisions = 0
collision_instances = 0

for i in range(len(outputs)):
	if "COLLISION" in outputs[i]:
		collision_instances += 1
		if ("COLLISION" not in outputs[i-1]) and ("COLLISION" not in outputs[i-3]):
			collisions += 1

print("Collisions: ", collisions, ", Collision instances: ", collision_instances)
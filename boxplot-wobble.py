import matplotlib.pyplot as plt
import numpy as np

num_moves_data_2 = [449/570, 325/877, 131/272, 199/746, 429/730, 379/935, 79/128, 76/121, 139/279, 339/896]

num_moves_data_3 = [249/533, 33/94, 57/194, 79/352, 152/427, 251/541, 395/944, 457/1008, 109/292, 264/817]

data = [num_moves_data_2, num_moves_data_3]

fig = plt.figure(figsize=(10,7))
ax = fig.add_axes([0.1,0.1,0.8,0.8])

bp = ax.boxplot(data)
plt.show()
import matplotlib.pyplot as plt
import numpy as np

num_moves_data_2 = [1140, 877, 1088, 746, 1460, 935, 1536, 1573, 1116, 896]

num_moves_data_3 = [1066, 846, 776, 704, 854, 1082, 944, 1008, 876, 817]

data = [num_moves_data_2, num_moves_data_3]

fig = plt.figure(figsize=(10,7))
ax = fig.add_axes([0.1,0.1,0.8,0.8])

bp = ax.boxplot(data)
plt.show()
import matplotlib.pyplot as plt
import numpy as np

num_moves_data_2 = [133, 128.8, 131.6, 3829/30, 2107/15, 1946/15, 137.2, 136.5, 392/3, 3899/30]

num_moves_data_3 = [1988/15, 128.1, 1918/15, 127.4, 385/3, 406/3, 128.1, 3857/30, 128.1, 3871/30]

data = [num_moves_data_2, num_moves_data_3]

fig = plt.figure(figsize=(10,7))
ax = fig.add_axes([0.1,0.1,0.8,0.8])

bp = ax.boxplot(data)
plt.show()
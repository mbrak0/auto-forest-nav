from tabulate import tabulate
table = [['Algorithm', 'Number of Moves', 'Euclidean Distance Travelled', 'Wobble Rate'], ['1', '1569', '142.57', '0.61058'], ['2', '854', '128.33', '0.35597'], ['3', '1349', '128.8', '0.59081'], ['4', '1613', '129.97', '0.65468']]
print(tabulate(table))
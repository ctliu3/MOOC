import numpy as np

L = np.matrix([[2, -1, -1, 0, 0, 0],
    [-1, 3, 0, -1, 0, -1],
    [-1, 0, 2, -1, 0, 0],
    [0, -1, -1, 3, -1, 0],
    [0, 0, 0, -1, 2, -1],
    [0, -1, 0, 0, -1, 2]])

# wrong
#eigvalues, eigvectors = np.linalg.eig(L)
#print eigvectors[:,1]

import numpy as np
import math

adj = np.array([
  [0, 0, 1],
  [0.5, 0, 0],
  [0.5, 1, 0]
  ])

def dist(r1, r2):
  ret = 0
  for i in xrange(r1.size):
    ret += math.fabs(r1[i] - r2[i])
  print ret
  return ret

eps = 1e-8
t = 0
r1 = np.array([1., 1., 1.])
r2 = np.zeros(3)
n = r1.size
#while dist(r1, r2) > eps:
while t < 6:
  if t > 0:
    r1 = np.copy(r2)
  r2 = np.zeros(3)
  for i in range(n):
    for j in range(n):
      r2[i] += r1[j] * adj[i, j]
  t += 1

print 't =', t
print r1

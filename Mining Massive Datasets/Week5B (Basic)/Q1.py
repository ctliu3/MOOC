
data = [
    [28, 145], [65, 140], [50, 130], [25, 125], [55, 118], [38, 115], [44, 105],
    [29, 97], [50, 90], [63, 88], [43, 83],
    [55, 63], [35, 63], [50, 60], [42, 57],
    [23, 40], [64, 37], [50, 30],
    [33, 22], [55, 20]
    ]
is_center = [0, 0, 0, 1, 0, 0, 1,
    1, 0, 0, 0,
    1, 1, 0, 1,
    1, 1, 0,
    1, 1
    ]

def getdis(p1, p2):
  x1 = p1[0] + 20
  x2 = p2[0] + 20
  return (x1 - x2) * (x1 - x2) + (p1[1] - p2[1]) * (p1[1] - p2[1])

n = len(is_center)
centers = []
unssign = []
for i in xrange (n):
  if is_center[i] == 1:
    centers.append(data[i])
  else:
    unssign.append(data[i])

ids = [0] * len(unssign)
for i in xrange(len(unssign)):
  mindis, idx = 1e9, 0
  for j in xrange(len(centers)):
    dis = getdis(unssign[i], centers[j])
    if dis < mindis:
      mindis, idx = dis, j
  ids[i] = idx

#print ids

# get new centers
for i in xrange(len(centers)):
  sx, sy = centers[i][0], centers[i][1]
  #print "@: ", sx, sy
  m = 1
  for j in xrange(len(unssign)):
    if ids[j] == i:
      sx += unssign[j][0]
      sy += unssign[j][1]
      m += 1
  print sx * 1. / m, sy * 1. / m

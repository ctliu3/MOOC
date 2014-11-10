s = [(0, 0), (10, 10)]
points = [(1, 6), (3, 7), (4, 3), (7, 7), (8, 2), (9, 5)]
n = len(points)

def dist((x1, y1), (x2, y2)):
  return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)

def get_mindis(point, s):
  mindis = 1e9
  for cur in s:
    curdis = dist(cur, point)
    if curdis < mindis:
      mindis = curdis
  return mindis

while n > 0:
  maxdis = -1e8
  idx = 0
  for i in xrange(n):
    dis = get_mindis(points[i], s)
    if dis > maxdis:
      maxdis, idx = dis, i
  print points[idx]
  s.append(points[idx])
  n -= 1
  del points[idx]


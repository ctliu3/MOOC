tbl = [[1, 2, 3, 4, 5], [2, 3, 2, 5, 3], [5, 5, 5, 3, 2]]

for i in xrange(3):
  ave = sum(tbl[i]) / 5.
  tbl[i] = [val - ave for val in tbl[i]]

for j in xrange(5):
  ave = 0
  for i in xrange(3):
    ave += tbl[i][j]
  ave /= 3.
  for i in xrange(3):
    tbl[i][j] -= ave

for i in xrange(3):
  for j in xrange(5):
    print "%.2f" % (tbl[i][j]),
  print

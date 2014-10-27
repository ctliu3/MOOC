import math
n = 4
a = [[3, 7, 8, 10], [4, 6, 9, 10], [1, 3, 6, 8], [1, 4, 7, 9]]
for i in xrange(n):
  mr = 0
  for j in xrange(n):
    val = (3 * a[i][j] + 7) % 11
    cnt = 0
    while (val & 1) == 0:
      val >>= 1
      cnt += 1
    mr = max(mr, cnt)
  print math.pow(2, mr)

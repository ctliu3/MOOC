mp = [0] * 10
for i in xrange(75):
  mp[i % 10] += 1

res1 = 0
for i in xrange(10):
  res1 += mp[i] * mp[i]
print res1

# 565
#tup = [25, 34, 47] # 675
#tup = [4, 31, 72] # 675
#tup = [3, 45, 72] # 525
#tup = [20, 49, 53] # 375
tup = [val - 1 for val in tup]
mp = [0] * 10

for i in xrange(tup[0], 75):
  val = i % 10
  if i < tup[1]:
    if val == tup[0] % 10:
      mp[val] += 1
  elif i < tup[2]:
    if val == tup[0] % 10 or val == tup[1] % 10:
      mp[val] += 1
  else:
    if val == tup[0] % 10 or val == tup[1] % 10 or val == tup[2] % 10:
      mp[val] += 1

res2 = []
for val in tup:
  if mp[val % 10] != 0:
    res2 += [75 * (2 * mp[val % 10] - 1)]
res2.sort()
print res2[1] 


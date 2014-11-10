import math

ctr = [
    [.015, .016, .017, .018, .019],
    [.010, .012, .014, .015, .016],
    [.005, .006, .007, .008, .010]
    ]
bid = [.10, .09, .08, .07, .06]
budget = [1, 2, 3, 4, 5]
click_through = [0] * 5
total = 101

while total > 0:
  ad = [0] * 3
  val = [-100] * 3
  for i in xrange(3):
    product = [ctr[i][j] * bid[j] for j in xrange(5)]

    for j in xrange(5):
      if product[j] > val[i]:
        val[i], ad[i] = product[j], j

  times = [0] * 3
  mint, ctr_val, idx = 1000, 0, 0
  for i in xrange(3):
    times[i] = math.floor(budget[ad[i]] * 1. / bid[ad[i]])
    if times[i] < mint:
      mint, ctr_val, idx = times[i], ctr[i][ad[i]], ad[i]

  if mint < 0:
    break
  mint = min(mint, total)
  bid[idx] = -100

  for i in xrange(3):
    nclick = round(ctr[i][ad[i]] * mint * 1. / ctr_val)
    budget[ad[i]] -= nclick * bid[ad[i]]
    click_through[ad[i]] += nclick
    total -= nclick

print click_through
print total

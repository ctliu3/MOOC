import math

def _map(val):
  def is_prime(a):
    for i in xrange(2, int(math.sqrt(a)) + 1):
      if (a % i) == 0:
        return False
    return True

  pair = []
  for i in xrange(2, int(math.sqrt(val)) + 1):
    if (val % i) == 0 and is_prime(i):
      pair.append((i, val))
  return pair

def reduce(pairs):
  mp = {}
  for (k, v) in pairs:
    if k not in mp:
      mp[k] = v
    else:
      mp[k] += v
  return mp

pairs = []
ints = [15, 21, 24, 30, 49]
for val in ints:
  pairs += _map(val)

print reduce(pairs)

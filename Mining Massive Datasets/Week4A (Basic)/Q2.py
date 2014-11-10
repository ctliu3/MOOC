from math import sqrt

A = [1, 0, 1, 0, 1]
B = [1, 1, 0, 0, 1]
C = [0, 1, 0, 1, 0]
rating = [2, 6, 2]

def cosine(va, vb, ra, rb, scale):
  dot_product = 0
  for i in xrange(len(va)):
    dot_product += va[i] * vb[i]
  return (dot_product + (ra * ra) + (rb * rb) * scale) / \
      sqrt((sum(va) + ra * ra * scale * scale) + (sum(vb) + rb * rb * scale * scale))

cur = 0.
print cosine(A, B, rating[0], rating[1], cur)
print cosine(A, C, rating[0], rating[2], cur)
print cosine(B, C, rating[1], rating[2], cur)

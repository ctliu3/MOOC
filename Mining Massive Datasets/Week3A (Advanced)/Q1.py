n = 8
edges = [(0, 2), (0, 5), (2, 3), (3, 4), (5, 6), (6, 7), (2, 5), (3, 6),
    (4, 7), (4, 1), (1, 7)]

def A(edges):
  adj = [[0 for _ in xrange(n)] for _ in xrange(n)]
  for (u, v) in edges:
    adj[u][v] = adj[v][u] = 1
  return adj

def D(adj):
  deg = [[0 for _ in xrange(n)] for _ in xrange(n)]
  for j in xrange(n):
    add = 0
    for i in xrange(n):
      add += adj[i][j]
    deg[j][j] = add
  return deg
      
def L(deg, adj):
  lap = [[0 for _ in xrange(n)] for _ in xrange(n)]
  for i in xrange(n):
    for j in xrange(n):
      lap[i][j] = deg[i][j] - adj[i][j]
  return lap

def getsum(matrix):
  res = 0
  for i in xrange(n):
    res += sum(matrix[i])
  return res

def nonzero(matrix):
  res = 0
  for i in xrange(n):
    res += sum([val != 0 for val in matrix[i]])
  return res

adj = A(edges)
deg = D(adj)
lap = L(deg, adj)
print getsum(adj)
print getsum(deg)
print getsum(lap)
print nonzero(deg)

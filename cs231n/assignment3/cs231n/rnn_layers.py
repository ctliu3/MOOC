import numpy as np


"""
This file defines layer types that are commonly used for recurrent neural
networks.
"""


def rnn_step_forward(x, prev_h, Wx, Wh, b):
  """
  Run the forward pass for a single timestep of a vanilla RNN that uses a tanh
  activation function.

  The input data has dimension D, the hidden state has dimension H, and we use
  a minibatch size of N.

  Inputs:
  - x: Input data for this timestep, of shape (N, D).
  - prev_h: Hidden state from previous timestep, of shape (N, H)
  - Wx: Weight matrix for input-to-hidden connections, of shape (D, H)
  - Wh: Weight matrix for hidden-to-hidden connections, of shape (H, H)
  - b: Biases of shape (H,)

  Returns a tuple of:
  - next_h: Next hidden state, of shape (N, H)
  - cache: Tuple of values needed for the backward pass.
  """
  next_h, cache = None, None
  ##############################################################################
  # TODO: Implement a single forward step for the vanilla RNN. Store the next  #
  # hidden state and any values you need for the backward pass in the next_h   #
  # and cache variables respectively.                                          #
  ##############################################################################
  next_h = np.tanh(x.dot(Wx) + prev_h.dot(Wh) + b)
  cache = (next_h, x, prev_h, Wx, Wh)
  ##############################################################################
  #                               END OF YOUR CODE                             #
  ##############################################################################
  return next_h, cache


def rnn_step_backward(dnext_h, cache):
  """
  Backward pass for a single timestep of a vanilla RNN.

  Inputs:
  - dnext_h: Gradient of loss with respect to next hidden state
  - cache: Cache object from the forward pass

  Returns a tuple of:
  - dx: Gradients of input data, of shape (N, D)
  - dprev_h: Gradients of previous hidden state, of shape (N, H)
  - dWx: Gradients of input-to-hidden weights, of shape (N, H)
  - dWh: Gradients of hidden-to-hidden weights, of shape (H, H)
  - db: Gradients of bias vector, of shape (H,)
  """
  dx, dprev_h, dWx, dWh, db = None, None, None, None, None
  ##############################################################################
  # TODO: Implement the backward pass for a single step of a vanilla RNN.      #
  #                                                                            #
  # HINT: For the tanh function, you can compute the local derivative in terms #
  # of the output value from tanh.                                             #
  ##############################################################################
  h, x, prev_h, Wx, Wh = cache
  d_tanh = 1. - h**2
  dx = (dnext_h * d_tanh).dot(Wx.T)
  dprev_h = (dnext_h * d_tanh).dot(Wh.T)
  dWx = x.T.dot(dnext_h * d_tanh)
  dWh = prev_h.T.dot(dnext_h * d_tanh)
  db = np.sum(dnext_h * d_tanh, axis=0)
  ##############################################################################
  #                               END OF YOUR CODE                             #
  ##############################################################################
  return dx, dprev_h, dWx, dWh, db


def rnn_forward(x, h0, Wx, Wh, b):
  """
  Run a vanilla RNN forward on an entire sequence of data. We assume an input
  sequence composed of T vectors, each of dimension D. The RNN uses a hidden
  size of H, and we work over a minibatch containing N sequences. After running
  the RNN forward, we return the hidden states for all timesteps.

  Inputs:
  - x: Input data for the entire timeseries, of shape (N, T, D).
  - h0: Initial hidden state, of shape (N, H)
  - Wx: Weight matrix for input-to-hidden connections, of shape (D, H)
  - Wh: Weight matrix for hidden-to-hidden connections, of shape (H, H)
  - b: Biases of shape (H,)

  Returns a tuple of:
  - h: Hidden states for the entire timeseries, of shape (N, T, H).
  - cache: Values needed in the backward pass
  """
  h, cache = None, None
  ##############################################################################
  # TODO: Implement forward pass for a vanilla RNN running on a sequence of    #
  # input data. You should use the rnn_step_forward function that you defined  #
  # above.                                                                     #
  ##############################################################################
  N, T, D = x.shape
  _, H = h0.shape
  h = np.zeros((N, T, H))
  prev_h = h0
  cache_t_list = {}
  for t in range(T):
      # Weights are shared, but not the hidden state
      next_h, cache_t_list[t] = rnn_step_forward(x[:, t, :].reshape(N, -1), prev_h, Wx, Wh, b)
      h[:, t, :] = next_h
      prev_h = next_h
  cache = (x, cache_t_list)
  ##############################################################################
  #                               END OF YOUR CODE                             #
  ##############################################################################
  return h, cache


def rnn_backward(dh, cache):
  """
  Compute the backward pass for a vanilla RNN over an entire sequence of data.

  Inputs:
  - dh: Upstream gradients of all hidden states, of shape (N, T, H)

  Returns a tuple of:
  - dx: Gradient of inputs, of shape (N, T, D)
  - dh0: Gradient of initial hidden state, of shape (N, H)
  - dWx: Gradient of input-to-hidden weights, of shape (D, H)
  - dWh: Gradient of hidden-to-hidden weights, of shape (H, H)
  - db: Gradient of biases, of shape (H,)
  """
  dx, dh0, dWx, dWh, db = None, None, None, None, None
  ##############################################################################
  # TODO: Implement the backward pass for a vanilla RNN running an entire      #
  # sequence of data. You should use the rnn_step_backward function that you   #
  # defined above.                                                             #
  ##############################################################################
  N, T, H = dh.shape
  x, cache_t_list = cache
  _, _, D = x.shape
  dprev_h = np.zeros((N, H))
  dx = np.zeros((N, T, D))
  dWx = np.zeros((D, H))
  dWh = np.zeros((H, H))
  db = np.zeros(H)
  for t in range(T - 1, -1, -1):
      cur = dh[:, t, :].reshape(N, -1) + dprev_h
      dx[:,t,:], dprev_h, dWx_, dWh_, db_ = rnn_step_backward(cur, cache_t_list[t])
      dWx += dWx_
      dWh += dWh_
      db += db_
  dh0 = dprev_h
  ##############################################################################
  #                               END OF YOUR CODE                             #
  ##############################################################################
  return dx, dh0, dWx, dWh, db


def word_embedding_forward(x, W):
  """
  Forward pass for word embeddings. We operate on minibatches of size N where
  each sequence has length T. We assume a vocabulary of V words, assigning each
  to a vector of dimension D.

  Inputs:
  - x: Integer array of shape (N, T) giving indices of words. Each element idx
    of x muxt be in the range 0 <= idx < V.
  - W: Weight matrix of shape (V, D) giving word vectors for all words.

  Returns a tuple of:
  - out: Array of shape (N, T, D) giving word vectors for all input words.
  - cache: Values needed for the backward pass
  """
  out, cache = None, None
  ##############################################################################
  # TODO: Implement the forward pass for word embeddings.                      #
  #                                                                            #
  # HINT: This should be very simple.                                          #
  ##############################################################################
  N, T = x.shape
  V, D = W.shape
  out = np.zeros((N, T, D))
  x_vec = np.zeros((N, T, V))
  for i in range(N):
      for j in range(T):
          x_vec[i, j, :] = np.zeros(V)
          x_vec[i, j, x[i, j]] = 1
          out[i, j, :] = x_vec[i, j, :].dot(W)
  cache = (x_vec, W)
  ##############################################################################
  #                               END OF YOUR CODE                             #
  ##############################################################################
  return out, cache


def word_embedding_backward(dout, cache):
  """
  Backward pass for word embeddings. We cannot back-propagate into the words
  since they are integers, so we only return gradient for the word embedding
  matrix.

  HINT: Look up the function np.add.at

  Inputs:
  - dout: Upstream gradients of shape (N, T, D)
  - cache: Values from the forward pass

  Returns:
  - dW: Gradient of word embedding matrix, of shape (V, D).
  """
  dW = None
  ##############################################################################
  # TODO: Implement the backward pass for word embeddings.                     #
  #                                                                            #
  # HINT: Look up the function np.add.at                                       #
  ##############################################################################
  x_vec, W = cache
  N, T, D = dout.shape
  _, _, V = x_vec.shape
  dW = np.zeros_like(W)
  dout = dout.reshape(-1, D)
  x_vec = x_vec.reshape(-1, V)
  dW = x_vec.T.dot(dout)
  ##############################################################################
  #                               END OF YOUR CODE                             #
  ##############################################################################
  return dW


def sigmoid(x):
  """
  A numerically stable version of the logistic sigmoid function.
  """
  pos_mask = (x >= 0)
  neg_mask = (x < 0)
  z = np.zeros_like(x)
  z[pos_mask] = np.exp(-x[pos_mask])
  z[neg_mask] = np.exp(x[neg_mask])
  top = np.ones_like(x)
  top[neg_mask] = z[neg_mask]
  return top / (1 + z)


def lstm_step_forward(x, prev_h, prev_c, Wx, Wh, b):
  """
  Forward pass for a single timestep of an LSTM.
  
  The input data has dimension D, the hidden state has dimension H, and we use
  a minibatch size of N.
  
  Inputs:
  - x: Input data, of shape (N, D)
  - prev_h: Previous hidden state, of shape (N, H)
  - prev_c: previous cell state, of shape (N, H)
  - Wx: Input-to-hidden weights, of shape (D, 4H)
  - Wh: Hidden-to-hidden weights, of shape (H, 4H)
  - b: Biases, of shape (4H,)
  
  Returns a tuple of:
  - next_h: Next hidden state, of shape (N, H)
  - next_c: Next cell state, of shape (N, H)
  - cache: Tuple of values needed for backward pass.
  """
  next_h, next_c, cache = None, None, None
  #############################################################################
  # TODO: Implement the forward pass for a single timestep of an LSTM.        #
  # You may want to use the numerically stable sigmoid implementation above.  #
  #############################################################################
  N, D = x.shape
  N, H = prev_h.shape
  i = sigmoid(x.dot(Wx[:, 0:H]) + prev_h.dot(Wh[:, 0:H]) + b[0:H])
  f = sigmoid(x.dot(Wx[:, H:2*H]) + prev_h.dot(Wh[:, H:2*H]) + b[H:2*H])
  o = sigmoid(x.dot(Wx[:, 2*H:3*H]) + prev_h.dot(Wh[:, 2*H:3*H]) + b[2*H:3*H])
  g = np.tanh(x.dot(Wx[:, 3*H:4*H]) + prev_h.dot(Wh[:, 3*H:4*H]) + b[3*H:4*H])
  next_c = prev_c * f + i * g
  next_h = np.tanh(next_c) * o
  cache = x, prev_c, prev_h, Wh, Wx, next_c, i, f, o, g
  ##############################################################################
  #                               END OF YOUR CODE                             #
  ##############################################################################
  return next_h, next_c, cache


def lstm_step_backward(dnext_h, dnext_c, cache):
  """
  Backward pass for a single timestep of an LSTM.

  Inputs:
  - dnext_h: Gradients of next hidden state, of shape (N, H)
  - dnext_c: Gradients of next cell state, of shape (N, H)
  - cache: Values from the forward pass

  Returns a tuple of:
  - dx: Gradient of input data, of shape (N, D)
  - dprev_h: Gradient of previous hidden state, of shape (N, H)
  - dprev_c: Gradient of previous cell state, of shape (N, H)
  - dWx: Gradient of input-to-hidden weights, of shape (D, 4H)
  - dWh: Gradient of hidden-to-hidden weights, of shape (H, 4H)
  - db: Gradient of biases, of shape (4H,)
  """
  dx, dh, dc, dWx, dWh, db = None, None, None, None, None, None
  #############################################################################
  # TODO: Implement the backward pass for a single timestep of an LSTM.       #
  #                                                                           #
  # HINT: For sigmoid and tanh you can compute local derivatives in terms of  #
  # the output value from the nonlinearity.                                   #
  #############################################################################
  def derivative_sigmoid(x):
      return x * (1 - x)

  def derivative_tanh(x):
      return 1 - x**2

  x, prev_c, prev_h, Wh, Wx, next_c, i, f, o, g = cache
  N, D = x.shape
  _, H = dnext_h.shape
  dx = np.zeros_like(x)
  dprev_h = np.zeros((N, H))
  dprev_c = np.zeros((N, H))
  dWx = np.zeros((D, 4 * H))
  dWh = np.zeros((H, 4 * H))
  db = np.zeros(4 * H)

  dprev_c = dnext_c * f
  # next_c -> next_h
  dnext_c_2 = dnext_h * o * derivative_tanh(np.tanh(next_c))

  dprev_c += dnext_c_2 * f

  do = dnext_h * np.tanh(next_c) * derivative_sigmoid(o)
  dg = (dnext_c + dnext_c_2) * i * derivative_tanh(g)
  di = (dnext_c + dnext_c_2) * g * derivative_sigmoid(i)
  df = (dnext_c + dnext_c_2) * prev_c * derivative_sigmoid(f)

  dWx[:, 0:H] = x.T.dot(di)
  dWx[:, H:2*H] = x.T.dot(df)
  dWx[:, 2*H:3*H] = x.T.dot(do)
  dWx[:, 3*H:4*H] = x.T.dot(dg)

  dWh[:, 0:H] = prev_h.T.dot(di)
  dWh[:, H:2*H] = prev_h.T.dot(df)
  dWh[:, 2*H:3*H] = prev_h.T.dot(do)
  dWh[:, 3*H:4*H] = prev_h.T.dot(dg)

  dx += di.dot(Wx[:, 0:H].T)
  dx += df.dot(Wx[:, H:2*H].T)
  dx += do.dot(Wx[:, 2*H:3*H].T)
  dx += dg.dot(Wx[:, 3*H:4*H].T)

  dprev_h += di.dot(Wh[:, 0:H].T)
  dprev_h += df.dot(Wh[:, H:2*H].T)
  dprev_h += do.dot(Wh[:, 2*H:3*H].T)
  dprev_h += dg.dot(Wh[:, 3*H:4*H].T)

  db[0:H] = np.sum(di, axis=0)
  db[H:2*H] = np.sum(df, axis=0)
  db[2*H:3*H] = np.sum(do, axis=0)
  db[3*H:4*H] = np.sum(dg, axis=0)
  ##############################################################################
  #                               END OF YOUR CODE                             #
  ##############################################################################

  return dx, dprev_h, dprev_c, dWx, dWh, db


def lstm_forward(x, h0, Wx, Wh, b):
  """
  Forward pass for an LSTM over an entire sequence of data. We assume an input
  sequence composed of T vectors, each of dimension D. The LSTM uses a hidden
  size of H, and we work over a minibatch containing N sequences. After running
  the LSTM forward, we return the hidden states for all timesteps.
  
  Note that the initial cell state is passed as input, but the initial cell
  state is set to zero. Also note that the cell state is not returned; it is
  an internal variable to the LSTM and is not accessed from outside.
  
  Inputs:
  - x: Input data of shape (N, T, D)
  - h0: Initial hidden state of shape (N, H)
  - Wx: Weights for input-to-hidden connections, of shape (D, 4H)
  - Wh: Weights for hidden-to-hidden connections, of shape (H, 4H)
  - b: Biases of shape (4H,)
  
  Returns a tuple of:
  - h: Hidden states for all timesteps of all sequences, of shape (N, T, H)
  - cache: Values needed for the backward pass.
  """
  h, cache = None, None
  #############################################################################
  # TODO: Implement the forward pass for an LSTM over an entire timeseries.   #
  # You should use the lstm_step_forward function that you just defined.      #
  #############################################################################
  N, T, D = x.shape
  _, H = h0.shape
  h = np.zeros((N, T, H))
  prev_h = h0
  prev_c = np.zeros((N, H))
  cache_t_list = {}
  for t in range(T):
      # Weights are shared, but not the hidden state
      next_h, next_c, cache_t_list[t] = lstm_step_forward(
              x[:, t, :].reshape(N, -1), prev_h, prev_c, Wx, Wh, b)
      h[:, t, :] = next_h
      prev_h = next_h
      prev_c = next_c
  cache = (x, cache_t_list)
  ##############################################################################
  #                               END OF YOUR CODE                             #
  ##############################################################################

  return h, cache


def lstm_backward(dh, cache):
  """
  Backward pass for an LSTM over an entire sequence of data.]
  
  Inputs:
  - dh: Upstream gradients of hidden states, of shape (N, T, H)
  - cache: Values from the forward pass
  
  Returns a tuple of:
  - dx: Gradient of input data of shape (N, T, D)
  - dh0: Gradient of initial hidden state of shape (N, H)
  - dWx: Gradient of input-to-hidden weight matrix of shape (D, 4H)
  - dWh: Gradient of hidden-to-hidden weight matrix of shape (H, 4H)
  - db: Gradient of biases, of shape (4H,)
  """
  dx, dh0, dWx, dWh, db = None, None, None, None, None
  #############################################################################
  # TODO: Implement the backward pass for an LSTM over an entire timeseries.  #
  # You should use the lstm_step_backward function that you just defined.     #
  #############################################################################
  N, T, H = dh.shape
  x, cache_t_list = cache
  _, _, D = x.shape
  dprev_h = np.zeros((N, H))
  dprev_c = np.zeros((N, H))
  dx = np.zeros((N, T, D))
  dWx = np.zeros((D, 4*H))
  dWh = np.zeros((H, 4*H))
  db = np.zeros(4*H)
  for t in range(T - 1, -1, -1):
      h = dh[:, t, :].reshape(N, -1) + dprev_h
      dx[:,t,:], dprev_h, dprev_c, dWx_, dWh_, db_ = lstm_step_backward(
              h, dprev_c, cache_t_list[t])
      dWx += dWx_
      dWh += dWh_
      db += db_
  dh0 = dprev_h
  ##############################################################################
  #                               END OF YOUR CODE                             #
  ##############################################################################
  return dx, dh0, dWx, dWh, db


def affine_forward(x, w, b):
  D, M = w.shape
  N = x.shape[0]
  xshape = x.shape
  x = x.reshape(N, -1)
  out = np.zeros((N, M))
  out = x.dot(w) + b
  x = x.reshape(xshape)
  cache = (x, w, b)
  return out, cache


def affine_backward(dout, cache):
  x, w, b = cache
  N = x.shape[0]
  D, M = w.shape

  dx = dout.dot(w.T)
  dx = dx.reshape(x.shape)
  dw = x.reshape(N, -1).T.dot(dout)
  db = np.sum(dout, axis=0)
  return dx, dw, db


def temporal_affine_forward(x, w, b):
  """
  Forward pass for a temporal affine layer. The input is a set of D-dimensional
  vectors arranged into a minibatch of N timeseries, each of length T. We use
  an affine function to transform each of those vectors into a new vector of
  dimension M.

  Inputs:
  - x: Input data of shape (N, T, D)
  - w: Weights of shape (D, M)
  - b: Biases of shape (M,)

  Returns a tuple of:
  - out: Output data of shape (N, T, M)
  - cache: Values needed for the backward pass
  """
  N, T, D = x.shape
  M = b.shape[0]
  out = x.reshape(N * T, D).dot(w).reshape(N, T, M) + b
  cache = x, w, b, out
  return out, cache


def temporal_affine_backward(dout, cache):
  """
  Backward pass for temporal affine layer.

  Input:
  - dout: Upstream gradients of shape (N, T, M)
  - cache: Values from forward pass

  Returns a tuple of:
  - dx: Gradient of input, of shape (N, T, D)
  - dw: Gradient of weights, of shape (D, M)
  - db: Gradient of biases, of shape (M,)
  """
  x, w, b, out = cache
  N, T, D = x.shape
  M = b.shape[0]

  dx = dout.reshape(N * T, M).dot(w.T).reshape(N, T, D)
  dw = dout.reshape(N * T, M).T.dot(x.reshape(N * T, D)).T
  db = dout.sum(axis=(0, 1))

  return dx, dw, db


def temporal_softmax_loss(x, y, mask, verbose=False):
  """
  A temporal version of softmax loss for use in RNNs. We assume that we are
  making predictions over a vocabulary of size V for each timestep of a
  timeseries of length T, over a minibatch of size N. The input x gives scores
  for all vocabulary elements at all timesteps, and y gives the indices of the
  ground-truth element at each timestep. We use a cross-entropy loss at each
  timestep, summing the loss over all timesteps and averaging across the
  minibatch.

  As an additional complication, we may want to ignore the model output at some
  timesteps, since sequences of different length may have been combined into a
  minibatch and padded with NULL tokens. The optional mask argument tells us
  which elements should contribute to the loss.

  Inputs:
  - x: Input scores, of shape (N, T, V)
  - y: Ground-truth indices, of shape (N, T) where each element is in the range
       0 <= y[i, t] < V
  - mask: Boolean array of shape (N, T) where mask[i, t] tells whether or not
    the scores at x[i, t] should contribute to the loss.

  Returns a tuple of:
  - loss: Scalar giving loss
  - dx: Gradient of loss with respect to scores x.
  """

  N, T, V = x.shape

  x_flat = x.reshape(N * T, V)
  y_flat = y.reshape(N * T)
  mask_flat = mask.reshape(N * T)

  probs = np.exp(x_flat - np.max(x_flat, axis=1, keepdims=True))
  probs /= np.sum(probs, axis=1, keepdims=True)
  loss = -np.sum(mask_flat * np.log(probs[np.arange(N * T), y_flat])) / N
  dx_flat = probs.copy()
  dx_flat[np.arange(N * T), y_flat] -= 1
  dx_flat /= N
  dx_flat *= mask_flat[:, None]

  if verbose: print 'dx_flat: ', dx_flat.shape

  dx = dx_flat.reshape(N, T, V)
  
  return loss, dx


import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train = X.shape[0]
  num_classes = W.shape[1]
  for i in range(num_train):
    f = np.dot(X[i], W)
    # Shift values of f for numeric stability
    f -= np.max(f)
    scores = np.exp(f)/np.sum(np.exp(f))
    loss += -np.log(scores[y[i]])
    for j in range(num_classes):
      if j == y[i]:
        dW[:, j] += (scores[j]-1.0)*X[i]
      else:
        dW[:, j] += (scores[j])*X[i]

  # Normalize loss
  loss /= num_train
  # Add L2 regularization
  loss += reg * np.sum(W * W)
  # Normalize gradient and add regularization gradient
  dW = dW/num_train + 2.0 * reg * W

  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train = X.shape[0]
  num_classes = W.shape[1]
  f = np.dot(X, W)
  # Shift values of f for numeric stability (separately for each training example)
  f -= np.max(f, axis=1, keepdims=True)
  scores = np.exp(f)/np.sum(np.exp(f), axis=1, keepdims=True)
  loss += -np.sum(np.log(scores[np.arange(num_train), y]))
  loss /= num_train
  loss += reg * np.sum(W * W)
  scores[np.arange(num_train), y] -= 1.0
  dW += np.dot(X.T, scores)
  dW = dW/num_train + 2.0 * reg * W

  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


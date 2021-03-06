import numpy as np
from random import shuffle
from past.builtins import xrange

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
  num_train=X.shape[0]
  num_classes=W.shape[1]

  for i in range(num_train):
    scores=X[i].dot(W)
    scores-=np.max(scores)
    scores=np.exp(scores)
    P=scores[y[i]]/np.sum(scores)
    loss+=-np.log(P)

    for j in range(num_classes):
      if j==y[i]:
        dW[:,j]+= -(1.0-P)*X[i]
      else:
        P_new=scores[j]/np.sum(scores)
        dW[:,j]+=P_new*X[i]

  loss/=num_train
  loss+=0.5*reg*np.sum(W*W)

  dW/=num_train
  dW+=reg*W

  pass
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.

  #Vectorised implementation is almost 3-5 times faster
  loss = 0.0
  dW = np.zeros_like(W)
  num_train=X.shape[0]
  num_classes=W.shape[1]

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################

  #   dW(k,c)=(summation over i=1-num_train) P(i,c)*X(i,k)   
  #   hence with some manipulation dW=X.T.dot(P-indices)

  scores=X.dot(W)
  scores-=np.max(scores,axis=1).reshape(-1,1)
  scores=np.exp(scores)
  Sum=np.sum(scores,axis=1).reshape(-1,1)
  P=scores/Sum
  
  loss=np.sum( -np.log(P[np.arange(num_train),y]) )

  indices=np.zeros_like(P)
  indices[np.arange(num_train),y]=1
  dW=X.T.dot(P-indices)

  loss/=num_train
  dW/=num_train
  loss+=0.5*reg*np.sum(W*W)
  dW+=reg*W

  pass
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


import numpy as np
from random import shuffle

def svm_loss_naive(W, X, y, reg):
  """
  Structured SVM loss function, naive implementation (with loops).

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
  #print W.shape,X[2].shape
  delta = 1.0
  dW = np.zeros(W.shape) # initialize the gradient as zero
  #print dW[:,1].shape
  # compute the loss and the gradient
  num_classes = W.shape[1]

  num_train = X.shape[0]
  loss = 0.0
  for i in xrange(num_train):
      scores = X[i].dot(W)
      correct_class_score = scores[y[i]]
      for j in xrange(num_classes):
          if j == y[i]:
              continue
          margin = scores[j] - correct_class_score + delta # note delta = 1
          if margin > 0:
              loss += margin
              dW[:,y[i]] = dW[:,y[i]] - np.transpose(X[i])
              dW[:,j] += np.transpose(X[i])
        

  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train
  dW /= num_train
  # Add regularization to the loss.
  #loss += 0.5 * reg * np.sum(W * W)
  loss += reg * np.sum(W * W)
  
  dW += reg*W


  #############################################################################
  # TODO:                                                                     #
  # Compute the gradient of the loss function and store it dW.                #
  # Rather that first computing the loss and then computing the derivative,   #
  # it may be simpler to compute the derivative at the same time that the     #
  # loss is being computed. As a result you may need to modify some of the    #
  # code above to compute the gradient.                                       #
  #############################################################################


  return loss, dW


def svm_loss_vectorized(W, X, y, reg):
  """
  Structured SVM loss function, vectorized implementation.

  Inputs and outputs are the same as svm_loss_naive.
  """
  loss = 0.0
  dW = np.zeros(W.shape) # initialize the gradient as zero
  delta = 1.0
  num_train = X.shape[0]
  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the structured SVM loss, storing the    #
  # result in loss.                                                           #
  #############################################################################
  scores = X.dot(W)
  
  correct_class_scores = scores[np.arange(num_train),y]
  #print correct_class_scores,correct_class_scores.shape
  margins = np.maximum(0, (scores.T - correct_class_scores + delta))
  #print margins.shape  
  margins[y,np.arange(num_train)] = 0
  
  
  
  positve_loss_count = np.sum(margins.T > 0, axis = 1)
  #print positve_loss_count
  #print scores.shape,margins.shape,positve_loss_count.shape
  #print margins.shape,y.shape  
  #margins[y] = 0
  #print scores[0],margins[0], y[0]
  
  
  
  loss = np.sum(margins)
  loss /= num_train
  #loss += 0.5 * reg * np.sum(W * W)
  loss += reg * np.sum(W * W)
  
  
  
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################


  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the gradient for the structured SVM     #
  # loss, storing the result in dW.                                           #
  #                                                                           #
  # Hint: Instead of computing the gradient from scratch, it may be easier    #
  # to reuse some of the intermediate values that you used to compute the     #
  # loss.                                                                     #
  #############################################################################
  
    
  loss_summary = np.zeros(scores.shape)
  #print scores.shape, loss_summary.shape, margins.shape , positve_loss_count.shape 
  loss_summary[margins.T > 0] = 1
  
  loss_summary[np.arange(num_train), y] = -1*positve_loss_count
  
  dW = np.dot(X.T, loss_summary)
  dW = dW / num_train + reg * W
  
    
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return loss, dW

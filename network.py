import tensorflow as tf
import utils

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

x = tf.placeholder(tf.float32, shape=[None, utils.POSITION_SIZE])
y_ = tf.placeholder(tf.float32, shape=[None, utils.MOVES_SIZE])


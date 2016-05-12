import tensorflow as tf
import utils

INPUT_NEURONS = 4
NUM_CLASSES = 4


# building the graph
def weight_variable(shape):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial)

def bias_variable(shape):
	initial = tf.constant(0.1, shape=shape)
	return tf.Variable(initial)

def placeholder_inputs(batch_size):
	'''
	These placeholders are used as inputs by the rest of the model building
	code and will be fed from the downloaded data in the .run() loop
	'''
	x_placeholder = tf.placeholder(tf.float32, shape=(batch_size, INPUT_NEURONS))
	y_placeholder = tf.placeholder(tf.float32, shape=(batch_size, NUM_CLASSES))
	return x_placeholder, y_placeholder


def feedforward(input_data, hidden1_units, hidden2_units):
	'''Building the graph that will be responsible for forward propagation
	Args:
		 input data
		 hidden_units: size of the given hidden layer
	Returns:
		 activation vector on the output layer
	'''

	# HIDDEN LAYER 1
	with tf.name_scope('hidden1'):

		weights1 = weight_variable((INPUT_NEURONS, hidden1_units))
		biases1 = bias_variable(hidden1_units)

		# dot product -> activation
		hidden1 = tf.nn.relu(tf.matmul(input_data, weights1) + biases1)

# HIDDEN LAYER 2
	with tf.name_scope('hidden2'):

		weights2 = weight_variable((hidden1_units, hidden2_units))
		biases2 = bias_variable(hidden2_units)

		# dot product -> activation
		hidden2 = tf.nn.relu(tf.matmul(hidden1, weights2) + biases2)

	with tf.name_scope('softmax_linear'):
		weigths3 = weight_variable((hidden2_units, NUM_CLASSES))      # moves_sizes = num of classes
		biases3 = bias_variable((NUM_CLASSES))

		logits = tf.matmul(hidden2, weights3) + biases3

	return logits


def loss(logits, labels):
	''' Further builds graph to calculate the loss from logits & and labels.
	Args:
		logits: Logits tensor, float of shape [batch_size, MOVES_SIZE]
		labels: Labels tensor, int32 of shape [MOVES_SIZE]
	Returns:
		loss tensor of type float
	'''

	# product 1-hot label
	labels = tf.to_int64(labels)
        # performs softmax + cross entropy - logits have to be of [batch_size, num_classes], and of float32 or float64 
        # labels have to be of [batch_size]
	cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
	logits, labels, name= 'xentropy')
	loss = tf.reduce_mean(cross_entropy, name='xentropy_mean')
	return loss

def training(loss, learning_rate):
	tf.scalar_summary(loss.op.name, loss)
	optimizer = tf.train.GradientDescentOptimizer(learning_rate)
	global_step = tf.Variable(0, name='global_step', trainable=False)
	train_op = optimizer.minimize(loss, global_step=global_step)
	return train_op


def evaluation(logits, labels):
	correct = tf.nn.in_top_k(logits, labels, 1)
	return tf.reduce_sum(tf.cast(correct, tf.int32))


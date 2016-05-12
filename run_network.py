import tensorflow as tf
import time

# import network helper functions
import network


BATCH_SIZE = 0
NUM_HIDDEN1 = 10
NUM_HIDDEN2 = 10
ETA = 0.5
EPOCHS = 30


def fill_dict(input_data, input_placeholder, label_placeholder):
    ''' Returns a dictionary of placeholders and input data'''
    input_data_pl, labels_pl = network.placeholder_inputs(BATCH_SIZE)

    feed_dict = {
        input_data: input_data_pl,
        labels : labels_pl
    }
    return feed_dict

def validate(sess,eval_correct,input_pl, labels_pl, data_set):
    '''Evaluates after each session/each epoch of data'''

    correct_count = 0
    dataset_size = len(data_set)
    batches = [data_set[k:k+BATCHSIZE] for k in xrange(0, dataset_size,BATCH_SIZE)]
    for batch in batches:
        feed_dict = fill_dict(data_set,
                              input_pl,
                              labels_pl)
        correct_count += sess.run(eval_correct, feed_dict=feed_dict)
    accuracy = correct_count / dataset_size
    print 'From %d examples: %d is correct. Precision: %0.04f'%(dataset_size, correct_count, accuracy)

def run_training():
    # TODO: read in data
    # training_data =
    # test_data = 

    with tf.Graph().as_default():
        input_pl, labels_pl = network.placeholder_inputs(BATCH_SIZE)
        logits = network.feedforward(training_data,
                                     NUM_HIDDEN1,
                                     NUM_HIDDEN2)

        loss = network.loss(logits, labels_pl)

        train_op = network.training(loss,ETA)

        eval_correct = network.evaluation(logits, labels_pl)
        # Build the summary operation based on the TF collection of Summaries.
        summary_op = tf.merge_all_summaries()

        # Create a saver for writing training checkpoints.
        saver = tf.train.Saver()

        # Create a session for running Ops on the Graph.
        sess = tf.Session()

        # Run the Op to initialize the variables.
        init = tf.initialize_all_variables()
        sess.run(init)

        # Instantiate a SummaryWriter to output summaries and the Graph.
        summary_writer = tf.train.SummaryWriter(FLAGS.train_dir, sess.graph)

        for epoch in xrange(EPOCHS):
            start_time = time.time()

            training_size = len(training_data)
            batches = [training_data[k:k+BATCHSIZE] for k in xrange(0, training_size,BATCH_SIZE)]
            for batch in batches:
                feed_dict = fill_dict(training_data,
                                      input_pl,
                                      labels_pl)
                _, loss_value = sess.run([train_op, loss], feed_dict = feed_dict)
                duration = time.time() - start_time

                # Write summarry after each 10 epochs
                if epoch % 10 == 0:
                    print 'Epoch %d: loss = %.2f (%.3f sec)'%(epoch, loss_value, duration)

                    summary_str = sess.run(summary_op, feed_dict=feed_dict)
                    summary_writer.add_summary(summary_str, epoch)
                    summary_writer.flush()
        print 'Evaluate with the validation set...'
        validate(sess,
                 eval_correct,
                 input_pl,
                 labels_pl,
                 test_data)

def main():
    run_training()

def __name__ = '__main__'
    tf.app.run()


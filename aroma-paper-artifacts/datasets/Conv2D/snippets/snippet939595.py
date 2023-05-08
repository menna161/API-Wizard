import tensorflow as tf
from tensorpack import *


def build_graph(self, image, label):
    image = tf.transpose(image, [0, 3, 1, 2])
    image = (image / 255.0)
    with argscope(Conv2D, activation=tf.nn.relu, kernel_size=3, padding='VALID'), argscope([Conv2D, MaxPooling], data_format='NCHW'):
        logits = LinearWrap(image).Conv2D('conv0', 32, padding='SAME').Conv2D('conv1', 32).MaxPooling('pool0', 2).Dropout(rate=0.25).Conv2D('conv2', 64, padding='SAME').Conv2D('conv3', 64).MaxPooling('pool1', 2).Dropout(rate=0.25).FullyConnected('fc1', 512, activation=tf.nn.relu).Dropout(rate=0.5).FullyConnected('linear', 10, activation=tf.identity)()
    cost = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=label)
    cost = tf.reduce_mean(cost, name='cost')
    wrong = tf.cast(tf.logical_not(tf.nn.in_top_k(logits, label, 1)), tf.float32, name='wrong')
    tf.reduce_mean(wrong, name='train_error')
    return cost

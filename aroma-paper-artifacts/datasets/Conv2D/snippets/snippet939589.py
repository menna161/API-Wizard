import tensorflow as tf
import numpy as np
from tensorpack import *


def build_graph(self, image, label):
    image = (image / 255.0)
    with argscope(Conv2D, activation=tf.nn.relu, kernel_size=3), argscope([Conv2D, MaxPooling], data_format='channels_first'):
        logits = LinearWrap(image).Conv2D('conv1_1', 64, kernel_size=11, strides=4, padding='VALID').MaxPooling('pool1', 3, 2).Conv2D('conv1_2', 192, kernel_size=5).MaxPooling('pool2', 3, 2).Conv2D('conv3', 384).Conv2D('conv4', 256).Conv2D('conv5', 256).MaxPooling('pool3', 3, 2).FullyConnected('fc6', 4096, activation=tf.nn.relu).Dropout('drop0', rate=0.5).FullyConnected('fc7', 4096, activation=tf.nn.relu).Dropout('drop1', rate=0.5).FullyConnected('fc8', 1000, activation=tf.identity)()
    cost = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=label)
    cost = tf.reduce_mean(cost, name='cost')
    return cost

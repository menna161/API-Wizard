import tensorflow as tf
import numpy as np
import sys
from tensorpack import *


def build_graph(self, image, label):
    image = (image / 255.0)
    with argscope(Conv2D, activation=tf.nn.relu, kernel_size=3), argscope([Conv2D, MaxPooling], data_format='channels_first'):
        logits = LinearWrap(image).Conv2D('conv1_1', 64).Conv2D('conv1_2', 64).MaxPooling('pool1', 2).Conv2D('conv2_1', 128).Conv2D('conv2_2', 128).MaxPooling('pool2', 2).Conv2D('conv3_1', 256).Conv2D('conv3_2', 256).Conv2D('conv3_3', 256).MaxPooling('pool3', 2).Conv2D('conv4_1', 512).Conv2D('conv4_2', 512).Conv2D('conv4_3', 512).MaxPooling('pool4', 2).Conv2D('conv5_1', 512).Conv2D('conv5_2', 512).Conv2D('conv5_3', 512).MaxPooling('pool5', 2).FullyConnected('fc6', 4096, activation=tf.nn.relu).FullyConnected('fc7', 4096, activation=tf.nn.relu).FullyConnected('fc8', 1000, activation=tf.identity)()
    cost = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=label)
    cost = tf.reduce_mean(cost, name='cost')
    return cost

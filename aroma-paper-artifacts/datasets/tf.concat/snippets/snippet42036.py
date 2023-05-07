import math
import random
import multiprocessing as mp
import base.batch as bat
from utils import *
from base.initializers import xavier_init
from attr_batch import generate_attribute_triple_batch_queue
from utils import save_embeddings
from losses import relation_logistic_loss, attribute_logistic_loss, relation_logistic_loss_wo_negs, attribute_logistic_loss_wo_negs, space_mapping_loss, alignment_loss, logistic_loss_wo_negs, orthogonal_loss


def conv(attr_hs, attr_as, attr_vs, dim, feature_map_size=2, kernel_size=[2, 4], activation=tf.nn.tanh, layer_num=2):
    attr_as = tf.reshape(attr_as, [(- 1), 1, dim])
    attr_vs = tf.reshape(attr_vs, [(- 1), 1, dim])
    input_avs = tf.concat([attr_as, attr_vs], 1)
    input_shape = input_avs.shape.as_list()
    input_layer = tf.reshape(input_avs, [(- 1), input_shape[1], input_shape[2], 1])
    _conv = input_layer
    _conv = tf.layers.batch_normalization(_conv, 2)
    for i in range(layer_num):
        _conv = tf.layers.conv2d(inputs=_conv, filters=feature_map_size, kernel_size=kernel_size, strides=[1, 1], padding='same', activation=activation)
    _conv = tf.nn.l2_normalize(_conv, 2)
    _shape = _conv.shape.as_list()
    _flat = tf.reshape(_conv, [(- 1), ((_shape[1] * _shape[2]) * _shape[3])])
    dense = tf.layers.dense(inputs=_flat, units=dim, activation=activation)
    dense = tf.nn.l2_normalize(dense)
    score = (- tf.reduce_sum(tf.square((attr_hs - dense)), 1))
    return score

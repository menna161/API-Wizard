import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from dps import cfg
from dps.utils import Param
from dps.utils.tf import build_scheduled_value, RenderHook, tf_mean_sum
from auto_yolo.models.core import VariationalAutoencoder, normal_vae, mAP, xent_loss, concrete_binary_pre_sigmoid_sample, concrete_binary_sample_kl


def _meshgrid(height, width):
    with tf.variable_scope('_meshgrid'):
        x_t = tf.matmul(tf.ones(shape=tf.stack([height, 1])), tf.transpose(tf.expand_dims(tf.linspace((- 1.0), 1.0, width), 1), [1, 0]))
        y_t = tf.matmul(tf.expand_dims(tf.linspace((- 1.0), 1.0, height), 1), tf.ones(shape=tf.stack([1, width])))
        x_t_flat = tf.reshape(x_t, (1, (- 1)))
        y_t_flat = tf.reshape(y_t, (1, (- 1)))
        ones = tf.ones_like(x_t_flat)
        grid = tf.concat(axis=0, values=[x_t_flat, y_t_flat, ones])
        return grid

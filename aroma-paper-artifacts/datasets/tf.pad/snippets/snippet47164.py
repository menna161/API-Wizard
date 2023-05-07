import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from dps import cfg
from dps.utils import Param
from dps.utils.tf import build_scheduled_value, RenderHook, tf_mean_sum
from auto_yolo.models.core import VariationalAutoencoder, normal_vae, mAP, xent_loss, concrete_binary_pre_sigmoid_sample, concrete_binary_sample_kl


def process_tensor_array(tensor_array, name, shape=None):
    tensor = tf.transpose(tensor_array.stack(), (1, 0, 2))
    time_pad = (self.max_time_steps - tf.shape(tensor)[1])
    padding = [[0, 0], [0, time_pad]]
    padding += ([[0, 0]] * (len(tensor.shape) - 2))
    tensor = tf.pad(tensor, padding, name=name)
    if (shape is not None):
        tensor = tf.reshape(tensor, shape)
    return tensor

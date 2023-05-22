import utils
import tensorflow as tf
import logging


@staticmethod
def multi_stroke_fusion(stylized_maps, attention_map, theta=50.0, mode='softmax'):
    stroke_num = len(stylized_maps)
    if (stroke_num == 1):
        return stylized_maps[0]
    one_channel_attention = tf.expand_dims(tf.reduce_mean(attention_map, axis=(- 1)), 3)
    centroids = utils.k_means(one_channel_attention, stroke_num)
    saliency_distances = []
    for i in range(stroke_num):
        saliency_distances.append(tf.abs((one_channel_attention - centroids[i])))
    multi_channel_saliency = tf.concat(saliency_distances, (- 1))
    if (mode == 'softmax'):
        multi_channel_saliency = tf.nn.softmax((theta * (1.0 - multi_channel_saliency)), (- 1))
    elif (mode == 'linear'):
        multi_channel_saliency = tf.div(multi_channel_saliency, tf.expand_dims(tf.reduce_sum(multi_channel_saliency, (- 1)), 3))
    else:
        pass
    finial_stylized_map = 0
    for i in range(stroke_num):
        temp = tf.expand_dims(multi_channel_saliency[(0, :, :, i)], 0)
        temp = tf.expand_dims(temp, 3)
        finial_stylized_map += tf.multiply(stylized_maps[i], temp)
    return (finial_stylized_map, centroids)

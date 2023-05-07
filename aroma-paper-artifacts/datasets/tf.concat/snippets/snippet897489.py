import tensorflow as tf
import vgg
from tensorflow.python.ops import control_flow_ops
import tensorflow.contrib.slim as slim
import cv2


def k_means(image, clusters_num):
    image = tf.squeeze(image)
    print('k_means', image.shape)
    _points = tf.reshape(image, ((- 1), 1))
    centroids = tf.slice(tf.random_shuffle(_points), [0, 0], [clusters_num, (- 1)])
    points_expanded = tf.expand_dims(_points, 0)
    for i in xrange(80):
        centroids_expanded = tf.expand_dims(centroids, 1)
        distances = tf.reduce_sum(tf.square(tf.subtract(points_expanded, centroids_expanded)), 2)
        assignments = tf.argmin(distances, 0)
        centroids = tf.concat([tf.reduce_mean(tf.gather(_points, tf.reshape(tf.where(tf.equal(assignments, c)), [1, (- 1)])), axis=1) for c in xrange(clusters_num)], 0)
    centroids = tf.squeeze(centroids)
    centroids = (- tf.nn.top_k((- centroids), clusters_num)[0])
    return centroids

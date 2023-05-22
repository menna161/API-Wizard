import tensorflow as tf
import vgg
from tensorflow.python.ops import control_flow_ops
import tensorflow.contrib.slim as slim
import cv2

if (__name__ == '__main__'):
    import cv2
    img = cv2.imread('lenna_cropped.jpg', cv2.IMREAD_GRAYSCALE)
    points = tf.cast(tf.convert_to_tensor(img), tf.float32)
    print(points.shape)
    centroids = k_means(points, 4)
    sess = tf.InteractiveSession()
    sess.run(tf.global_variables_initializer())
    print(sess.run(centroids))

from networks import generator
import tensorflow as tf
from PIL import Image
import numpy as np
import os


def generate_fixed_z():
    label = tf.placeholder(tf.float32, [None, NUMS_CLASS])
    z = tf.placeholder(tf.float32, [None, 100])
    labeled_z = tf.concat([z, label], axis=1)
    G = generator('generator')
    fake_img = G(labeled_z)
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver()
    saver.restore(sess, './save_para/model.ckpt')
    (LABELS, Z) = label_from_0_to_1()
    if (not os.path.exists('./generate_fixed_noise')):
        os.mkdir('./generate_fixed_noise')
    FAKE_IMG = sess.run(fake_img, feed_dict={label: LABELS, z: Z})
    for i in range(10):
        Image.fromarray(np.uint8(((FAKE_IMG[(i, :, :, :)] + 1) * 127.5))).save((('./generate_fixed_noise/' + str(i)) + '.jpg'))

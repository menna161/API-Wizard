from networks import generator
import tensorflow as tf
from PIL import Image
import numpy as np
import os


def generate_fixed_label():
    label = tf.placeholder(tf.int32, [None])
    z = tf.placeholder(tf.float32, [None, 100])
    one_hot_label = tf.one_hot(label, NUMS_CLASS)
    labeled_z = tf.concat([z, one_hot_label], axis=1)
    G = generator('generator')
    fake_img = G(labeled_z)
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver()
    saver.restore(sess, './save_para/model.ckpt')
    Z = from_noise0_to_noise1()
    LABELS = np.ones([10])
    if (not os.path.exists('./generate_fixed_label')):
        os.mkdir('./generate_fixed_label')
    FAKE_IMG = sess.run(fake_img, feed_dict={label: LABELS, z: Z})
    for i in range(10):
        Image.fromarray(np.uint8(((FAKE_IMG[(i, :, :, :)] + 1) * 127.5))).save((((('./generate_fixed_label/' + str(i)) + '_') + str(int(LABELS[i]))) + '.jpg'))

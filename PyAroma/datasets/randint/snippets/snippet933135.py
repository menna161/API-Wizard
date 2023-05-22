import tensorflow as tf
import numpy as np
import os
from PIL import Image
import scipy.misc as misc
import matplotlib.pyplot as plt
import time


def test(self):
    list_ = os.listdir('./maps/val/')
    nums_file = list_.__len__()
    saver = tf.train.Saver(tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, 'generator'))
    saver.restore(self.sess, './save_para/model.ckpt')
    rand_select = np.random.randint(0, nums_file)
    INPUTS_CONDITION = np.zeros([1, self.img_h, self.img_w, 3])
    INPUTS = np.zeros([1, self.img_h, self.img_w, 3])
    img = np.array(Image.open((self.path + list_[rand_select])))
    (img_h, img_w) = (img.shape[0], img.shape[1])
    INPUTS_CONDITION[0] = ((misc.imresize(img[(:, (img_w // 2):)], [self.img_h, self.img_w]) / 127.5) - 1.0)
    INPUTS[0] = ((misc.imresize(img[(:, :(img_w // 2))], [self.img_h, self.img_w]) / 127.5) - 1.0)
    [fake_img] = self.sess.run([self.inputs_fake], feed_dict={self.inputs_condition: INPUTS_CONDITION})
    out_img = np.concatenate((INPUTS_CONDITION[0], fake_img[0], INPUTS[0]), axis=1)
    plt.imshow(np.uint8(((out_img + 1.0) * 127.5)))
    plt.grid('off')
    plt.axis('off')
    plt.show()

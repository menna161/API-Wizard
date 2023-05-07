import tensorflow as tf
import numpy as np
import os
from PIL import Image
import scipy.misc as misc


def train(self):
    list = os.listdir(self.path)
    nums_file = list.__len__()
    saver = tf.train.Saver()
    for i in range(10000):
        rand_select = np.random.randint(0, nums_file, [self.batch_size])
        INPUTS = np.zeros([self.batch_size, self.img_h, self.img_w, 3])
        INPUTS_CONDITION = np.zeros([self.batch_size, self.img_h, self.img_w, 3])
        for j in range(self.batch_size):
            img = np.array(Image.open((self.path + list[rand_select[j]])))
            (img_h, img_w) = (img.shape[0], img.shape[1])
            INPUTS_CONDITION[j] = ((misc.imresize(img[(:, :(img_w // 2))], [self.img_h, self.img_w]) / 127.5) - 1.0)
            INPUTS[j] = ((misc.imresize(img[(:, (img_w // 2):)], [self.img_h, self.img_w]) / 127.5) - 1.0)
        self.sess.run(self.opt_dis, feed_dict={self.inputs: INPUTS, self.inputs_condition: INPUTS_CONDITION})
        self.sess.run(self.opt_gen, feed_dict={self.inputs: INPUTS, self.inputs_condition: INPUTS_CONDITION})
        if ((i % 10) == 0):
            [G_LOSS, D_LOSS] = self.sess.run([self.g_loss, self.d_loss], feed_dict={self.inputs: INPUTS, self.inputs_condition: INPUTS_CONDITION})
            print(('Iteration: %d, d_loss: %f, g_loss: %f' % (i, D_LOSS, G_LOSS)))
        if ((i % 100) == 0):
            saver.save(self.sess, './save_para//model.ckpt')

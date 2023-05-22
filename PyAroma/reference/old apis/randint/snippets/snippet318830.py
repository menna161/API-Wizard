from __future__ import division
import math
import json
import random
import pprint
import scipy.misc
import numpy as np
from time import gmtime, strftime
from six.moves import xrange
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.contrib.slim as slim
from numpy.lib.stride_tricks import as_strided
import numbers
import moviepy.editor as mpy


def visualize(sess, dcgan, config, option):
    image_frame_dim = int(math.ceil((config.batch_size ** 0.5)))
    if (option == 0):
        z_sample = np.random.uniform((- 0.5), 0.5, size=(config.batch_size, dcgan.z_dim))
        samples = sess.run(dcgan.sampler, feed_dict={dcgan.z: z_sample})
        save_images(samples, [image_frame_dim, image_frame_dim], ('./samples/test_%s.png' % strftime('%Y%m%d%H%M%S', gmtime())))
    elif (option == 1):
        values = np.arange(0, 1, (1.0 / config.batch_size))
        for idx in xrange(100):
            print((' [*] %d' % idx))
            z_sample = np.zeros([config.batch_size, dcgan.z_dim])
            for (kdx, z) in enumerate(z_sample):
                z[idx] = values[kdx]
            if (config.dataset == 'mnist'):
                y = np.random.choice(10, config.batch_size)
                y_one_hot = np.zeros((config.batch_size, 10))
                y_one_hot[(np.arange(config.batch_size), y)] = 1
                samples = sess.run(dcgan.sampler, feed_dict={dcgan.z: z_sample, dcgan.y: y_one_hot})
            else:
                samples = sess.run(dcgan.sampler, feed_dict={dcgan.z: z_sample})
            save_images(samples, [image_frame_dim, image_frame_dim], ('./samples/test_arange_%s.png' % idx))
    elif (option == 2):
        values = np.arange(0, 1, (1.0 / config.batch_size))
        for idx in [random.randint(0, 99) for _ in xrange(100)]:
            print((' [*] %d' % idx))
            z = np.random.uniform((- 0.2), 0.2, size=dcgan.z_dim)
            z_sample = np.tile(z, (config.batch_size, 1))
            for (kdx, z) in enumerate(z_sample):
                z[idx] = values[kdx]
            if (config.dataset == 'mnist'):
                y = np.random.choice(10, config.batch_size)
                y_one_hot = np.zeros((config.batch_size, 10))
                y_one_hot[(np.arange(config.batch_size), y)] = 1
                samples = sess.run(dcgan.sampler, feed_dict={dcgan.z: z_sample, dcgan.y: y_one_hot})
            else:
                samples = sess.run(dcgan.sampler, feed_dict={dcgan.z: z_sample})
            try:
                make_gif(samples, ('./samples/test_gif_%s.gif' % idx))
            except:
                save_images(samples, [image_frame_dim, image_frame_dim], ('./samples/test_%s.png' % strftime('%Y%m%d%H%M%S', gmtime())))
    elif (option == 3):
        values = np.arange(0, 1, (1.0 / config.batch_size))
        for idx in xrange(100):
            print((' [*] %d' % idx))
            z_sample = np.zeros([config.batch_size, dcgan.z_dim])
            for (kdx, z) in enumerate(z_sample):
                z[idx] = values[kdx]
            samples = sess.run(dcgan.sampler, feed_dict={dcgan.z: z_sample})
            make_gif(samples, ('./samples/test_gif_%s.gif' % idx))
    elif (option == 4):
        image_set = []
        values = np.arange(0, 1, (1.0 / config.batch_size))
        for idx in xrange(100):
            print((' [*] %d' % idx))
            z_sample = np.zeros([config.batch_size, dcgan.z_dim])
            for (kdx, z) in enumerate(z_sample):
                z[idx] = values[kdx]
            image_set.append(sess.run(dcgan.sampler, feed_dict={dcgan.z: z_sample}))
            make_gif(image_set[(- 1)], ('./samples/test_gif_%s.gif' % idx))
        new_image_set = [merge(np.array([images[idx] for images in image_set]), [10, 10]) for idx in (range(64) + range(63, (- 1), (- 1)))]
        make_gif(new_image_set, './samples/test_gif_merged.gif', duration=8)

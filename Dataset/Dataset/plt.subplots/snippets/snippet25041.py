import code
import random
import imageio
import tensorflow as tf
import tensorflow_addons as tfa
import matplotlib.pyplot as plt
from ccn.cfg import get_config
from ccn.ml_utils import gaussian_k
from ccn.experimental_aug import transform_batch
import os

if (__name__ == '__main__'):
    import os
    os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
    os.environ['CUDA_VISIBLE_DEVICES'] = ''
    img = imageio.imread('kitty.jpg')
    img = (tf.cast(img, tf.float32) / 255.0)
    imgs = tf.tile(img[tf.newaxis], [4, 1, 1, 1])
    channel = get_noisy_channel()
    for diff in tf.range(16):
        print(diff)
        x = channel(imgs, diff)
        (fig, axes) = plt.subplots(2, 2)
        x = (x - tf.math.reduce_min(x))
        x = (x / tf.math.reduce_max(x))
        axes[0][0].imshow(x[0])
        axes[0][1].imshow(x[1])
        axes[1][0].imshow(x[2])
        axes[1][1].imshow(x[3])
        plt.savefig(f'noise_{diff}.png')

import math
import code
import tensorflow as tf
import matplotlib.pyplot as plt
import os

if (__name__ == '__main__'):
    import os
    os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
    os.environ['CUDA_VISIBLE_DEVICES'] = ''
    x = tf.random.normal((4, 100, 100, 3))
    x = (x - tf.math.reduce_min(x))
    x = (x / tf.math.reduce_max(x))
    x_aug = transform(x)
    (fig, axes) = plt.subplots(4, 2)
    for b in range(4):
        img = x[b]
        img_aug = x_aug[b]
        axes[b][0].imshow(img)
        axes[b][1].imshow(img_aug)
    plt.show()

import tensorflow as tf
from core.models.vgg import VGG
from configuration import NUM_CLASSES, STAGE_BOXES_PER_PIXEL


def __init__(self):
    super(ExtraLayer, self).__init__()
    self.conv1 = tf.keras.layers.Conv2D(filters=256, kernel_size=1, strides=1, padding='same')
    self.conv2 = tf.keras.layers.Conv2D(filters=512, kernel_size=3, strides=2, padding='same')
    self.conv3 = tf.keras.layers.Conv2D(filters=128, kernel_size=1, strides=1, padding='same')
    self.conv4 = tf.keras.layers.Conv2D(filters=256, kernel_size=3, strides=2, padding='same')
    self.conv5 = tf.keras.layers.Conv2D(filters=128, kernel_size=1, strides=1, padding='same')
    self.conv6 = tf.keras.layers.Conv2D(filters=256, kernel_size=3, strides=1, padding='valid')
    self.conv7 = tf.keras.layers.Conv2D(filters=128, kernel_size=1, strides=1, padding='same')
    self.conv8 = tf.keras.layers.Conv2D(filters=256, kernel_size=3, strides=1, padding='valid')

import tensorflow as tf
from core.models.vgg import VGG
from configuration import NUM_CLASSES, STAGE_BOXES_PER_PIXEL


def _make_loc_conf(self, num_classes):
    loc_layers = list()
    conf_layers = list()
    for i in self.stage_boxes_per_pixel:
        loc_layers.append(tf.keras.layers.Conv2D(filters=(i * 4), kernel_size=3, strides=1, padding='same'))
        conf_layers.append(tf.keras.layers.Conv2D(filters=(i * num_classes), kernel_size=3, strides=1, padding='same'))
    return (loc_layers, conf_layers)

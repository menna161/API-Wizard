import tensorflow as tf
from core.models.vgg import VGG
from configuration import NUM_CLASSES, STAGE_BOXES_PER_PIXEL


def call(self, inputs, training=None, mask=None):
    sources = list()
    loc = list()
    conf = list()
    (x1, x) = self.backbone(inputs, training=training)
    x1 = self.l2_norm(x1)
    sources.append(x1)
    sources.append(x)
    (o1, o2, o3, o4) = self.extras(x)
    sources.extend([o1, o2, o3, o4])
    x = o4
    for (x, l, c) in zip(sources, self.locs, self.confs):
        loc.append(l(x))
        conf.append(c(x))
    loc = tf.concat(values=[tf.reshape(o, shape=(o.shape[0], (- 1))) for o in loc], axis=1)
    conf = tf.concat(values=[tf.reshape(o, shape=(o.shape[0], (- 1))) for o in conf], axis=1)
    loc = tf.reshape(loc, shape=(loc.shape[0], (- 1), 4))
    conf = tf.reshape(conf, shape=(conf.shape[0], (- 1), self.num_classes))
    return (loc, conf)

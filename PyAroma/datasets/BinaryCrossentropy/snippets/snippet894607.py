import tensorflow as tf
import keras.backend as K
from keras.losses import binary_crossentropy, BinaryCrossentropy


def basnet_hybrid_loss(self, y_true, y_pred):
    '\n        Hybrid loss proposed in BASNET (https://arxiv.org/pdf/2101.04704.pdf)\n        The hybrid loss is a combination of the binary cross entropy, structural similarity\n        and intersection-over-union losses, which guide the network to learn\n        three-level (i.e., pixel-, patch- and map- level) hierarchy representations.\n        '
    bce_loss = BinaryCrossentropy(from_logits=False)
    bce_loss = bce_loss(y_true, y_pred)
    ms_ssim_loss = self.ssim_loss(y_true, y_pred)
    jacard_loss = self.jacard_loss(y_true, y_pred)
    return ((bce_loss + ms_ssim_loss) + jacard_loss)

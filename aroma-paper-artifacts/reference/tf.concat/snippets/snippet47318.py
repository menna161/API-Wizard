import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from dps import cfg
from dps.utils.tf import tf_mean_sum, RenderHook
from auto_yolo.models.core import xent_loss, normal_vae, VariationalAutoencoder


def build_representation(self):
    if (self.encoder is None):
        self.encoder = cfg.build_encoder(scope='encoder')
        if ('encoder' in self.fixed_weights):
            self.encoder.fix_variables()
    if (self.decoder is None):
        self.decoder = cfg.build_decoder(scope='decoder')
        if ('decoder' in self.fixed_weights):
            self.decoder.fix_variables()
    attr = self.encoder(self.inp, (2 * self.A), self.is_training)
    (attr_mean, attr_log_std) = tf.split(attr, 2, axis=(- 1))
    attr_std = tf.exp(attr_log_std)
    if (not self.noisy):
        attr_std = tf.zeros_like(attr_std)
    (attr, attr_kl) = normal_vae(attr_mean, attr_std, self.attr_prior_mean, self.attr_prior_std)
    obj_shape = tf.concat([tf.shape(attr)[:(- 1)], [1]], axis=0)
    self._tensors['obj'] = tf.ones(obj_shape)
    self._tensors.update(attr_mean=attr_mean, attr_std=attr_std, attr_kl=attr_kl, attr=attr)
    reconstruction = self.decoder(attr, 3, self.is_training)
    reconstruction = reconstruction[(:, :self.inp.shape[1], :self.inp.shape[2], :)]
    reconstruction = tf.nn.sigmoid(tf.clip_by_value(reconstruction, (- 10), 10))
    self._tensors['output'] = reconstruction
    if self.train_kl:
        self.losses['attr_kl'] = tf_mean_sum(self._tensors['attr_kl'])
    if self.train_reconstruction:
        self._tensors['per_pixel_reconstruction_loss'] = xent_loss(pred=reconstruction, label=self.inp)
        self.losses['reconstruction'] = tf_mean_sum(self._tensors['per_pixel_reconstruction_loss'])

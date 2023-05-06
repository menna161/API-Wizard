import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from dps import cfg
from dps.utils import Param
from dps.utils.tf import build_scheduled_value, RenderHook, tf_mean_sum
from auto_yolo.models.core import VariationalAutoencoder, normal_vae, mAP, xent_loss, concrete_binary_pre_sigmoid_sample, concrete_binary_sample_kl


def body(step, stopping_sum, prev_state, running_recon, kl_loss, running_digits, scale_ta, scale_kl_ta, scale_std_ta, shift_ta, shift_kl_ta, shift_std_ta, attr_ta, attr_kl_ta, attr_std_ta, z_pres_ta, z_pres_probs_ta, z_pres_kl_ta, vae_input_ta, vae_output_ta, scale, shift, attr, z_pres):
    if self.difference_air:
        inp = (self._tensors['inp'] - tf.reshape(running_recon, (self.batch_size, *self.obs_shape)))
        encoded_inp = self.image_encoder(inp, 0, self.is_training)
        encoded_inp = tf.layers.flatten(encoded_inp)
    else:
        encoded_inp = self.encoded_inp
    if self.complete_rnn_input:
        rnn_input = tf.concat([encoded_inp, scale, shift, attr, z_pres], axis=1)
    else:
        rnn_input = encoded_inp
    (hidden_rep, next_state) = self.cell(rnn_input, prev_state)
    outputs = self.output_network(hidden_rep, 9, self.is_training)
    (scale_mean, scale_log_std, shift_mean, shift_log_std, z_pres_log_odds) = tf.split(outputs, [2, 2, 2, 2, 1], axis=1)
    scale_std = tf.exp(scale_log_std)
    scale_mean = self.apply_fixed_value('scale_mean', scale_mean)
    scale_std = self.apply_fixed_value('scale_std', scale_std)
    (scale_logits, scale_kl) = normal_vae(scale_mean, scale_std, self.scale_prior_mean, self.scale_prior_std)
    scale_kl = tf.reduce_sum(scale_kl, axis=1, keepdims=True)
    scale = tf.nn.sigmoid(tf.clip_by_value(scale_logits, (- 10), 10))
    shift_std = tf.exp(shift_log_std)
    shift_mean = self.apply_fixed_value('shift_mean', shift_mean)
    shift_std = self.apply_fixed_value('shift_std', shift_std)
    (shift_logits, shift_kl) = normal_vae(shift_mean, shift_std, self.shift_prior_mean, self.shift_prior_std)
    shift_kl = tf.reduce_sum(shift_kl, axis=1, keepdims=True)
    shift = tf.nn.tanh(tf.clip_by_value(shift_logits, (- 10), 10))
    (w, h) = (scale[(:, 0:1)], scale[(:, 1:2)])
    (x, y) = (shift[(:, 0:1)], shift[(:, 1:2)])
    theta = tf.concat([w, tf.zeros_like(w), x, tf.zeros_like(h), h, y], axis=1)
    theta = tf.reshape(theta, ((- 1), 2, 3))
    vae_input = transformer(self._tensors['inp'], theta, self.object_shape)
    vae_input = tf.reshape(vae_input, (self.batch_size, *self.object_shape, self.image_depth))
    attr = self.object_encoder(vae_input, (2 * self.A), self.is_training)
    (attr_mean, attr_log_std) = tf.split(attr, 2, axis=1)
    attr_std = tf.exp(attr_log_std)
    (attr, attr_kl) = normal_vae(attr_mean, attr_std, self.attr_prior_mean, self.attr_prior_std)
    attr_kl = tf.reduce_sum(attr_kl, axis=1, keepdims=True)
    vae_output = self.object_decoder(attr, ((self.object_shape[0] * self.object_shape[1]) * self.image_depth), self.is_training)
    vae_output = tf.nn.sigmoid(tf.clip_by_value(vae_output, (- 10), 10))
    theta_inverse = tf.concat([(1.0 / w), tf.zeros_like(w), ((- x) / w), tf.zeros_like(h), (1.0 / h), ((- y) / h)], axis=1)
    theta_inverse = tf.reshape(theta_inverse, ((- 1), 2, 3))
    vae_output_transformed = transformer(tf.reshape(vae_output, (self.batch_size, *self.object_shape, self.image_depth)), theta_inverse, self.obs_shape[:2])
    vae_output_transformed = tf.reshape(vae_output_transformed, [self.batch_size, ((self.image_height * self.image_width) * self.image_depth)])
    if self.run_all_time_steps:
        z_pres = tf.ones_like(z_pres_log_odds)
        z_pres_prob = tf.ones_like(z_pres_log_odds)
        z_pres_kl = tf.zeros_like(z_pres_log_odds)
    else:
        z_pres_log_odds = tf.clip_by_value(z_pres_log_odds, (- 10), 10)
        z_pres_pre_sigmoid = concrete_binary_pre_sigmoid_sample(z_pres_log_odds, self.z_pres_temperature)
        z_pres = tf.nn.sigmoid(z_pres_pre_sigmoid)
        z_pres = ((self.float_is_training * z_pres) + ((1 - self.float_is_training) * tf.round(z_pres)))
        z_pres_prob = tf.nn.sigmoid(z_pres_log_odds)
        z_pres_kl = concrete_binary_sample_kl(z_pres_pre_sigmoid, z_pres_log_odds, self.z_pres_temperature, self.z_pres_prior_log_odds, self.z_pres_temperature)
    stopping_sum += (1.0 - z_pres)
    alive = tf.less(stopping_sum, self.stopping_threshold)
    running_digits += tf.to_int32(alive)
    running_recon += tf.where(tf.tile(alive, (1, vae_output_transformed.shape[1])), (z_pres * vae_output_transformed), tf.zeros_like(running_recon))
    kl_loss += tf.where(alive, scale_kl, tf.zeros_like(kl_loss))
    kl_loss += tf.where(alive, shift_kl, tf.zeros_like(kl_loss))
    kl_loss += tf.where(alive, attr_kl, tf.zeros_like(kl_loss))
    kl_loss += tf.where(alive, z_pres_kl, tf.zeros_like(kl_loss))
    scale_ta = scale_ta.write(scale_ta.size(), scale)
    scale_kl_ta = scale_kl_ta.write(scale_kl_ta.size(), scale_kl)
    scale_std_ta = scale_std_ta.write(scale_std_ta.size(), scale_std)
    shift_ta = shift_ta.write(shift_ta.size(), shift)
    shift_kl_ta = shift_kl_ta.write(shift_kl_ta.size(), shift_kl)
    shift_std_ta = shift_std_ta.write(shift_std_ta.size(), shift_std)
    attr_ta = attr_ta.write(attr_ta.size(), attr)
    attr_kl_ta = attr_kl_ta.write(attr_kl_ta.size(), attr_kl)
    attr_std_ta = attr_std_ta.write(attr_std_ta.size(), attr_std)
    vae_input_ta = vae_input_ta.write(vae_input_ta.size(), tf.layers.flatten(vae_input))
    vae_output_ta = vae_output_ta.write(vae_output_ta.size(), vae_output)
    z_pres_ta = z_pres_ta.write(z_pres_ta.size(), z_pres)
    z_pres_probs_ta = z_pres_probs_ta.write(z_pres_probs_ta.size(), z_pres_prob)
    z_pres_kl_ta = z_pres_kl_ta.write(z_pres_kl_ta.size(), z_pres_kl)
    return ((step + 1), stopping_sum, next_state, running_recon, kl_loss, running_digits, scale_ta, scale_kl_ta, scale_std_ta, shift_ta, shift_kl_ta, shift_std_ta, attr_ta, attr_kl_ta, attr_std_ta, z_pres_ta, z_pres_probs_ta, z_pres_kl_ta, vae_input_ta, vae_output_ta, scale, shift, attr, z_pres)

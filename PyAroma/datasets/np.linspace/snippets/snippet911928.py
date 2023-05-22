from pathsetup import run_path_setup
import time
import pickle
import tensorflow as tf
import numpy as np
import utils
import gl
import os
from tqdm import tqdm
from nltk.tokenize import word_tokenize
from tensorflow.python.layers.core import Dense
from snli.decoder import basic_decoder
from scipy.stats import logistic


def linear_interpolate(self, checkpoint, num_samples):
    sampled = []
    for i in range((self.batch_size // num_samples)):
        z = np.random.normal(0, 1, (2, self.latent_dim))
        s1_z = z[0]
        s2_z = z[1]
        s1_z = np.repeat(s1_z[(None, :)], num_samples, axis=0)
        s2_z = np.repeat(s2_z[(None, :)], num_samples, axis=0)
        steps = np.linspace(0, 1, num_samples)[(:, None)]
        sampled.append(((s1_z * (1 - steps)) + (s2_z * steps)))
    sampled = np.reshape(np.array(sampled), newshape=(self.batch_size, self.latent_dim))
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess, checkpoint)
        result = sess.run(self.inference_logits, feed_dict={self.z_vector: sampled, self.keep_prob: 1.0, self.z_temperature: self.z_temp})
        for (i, pred) in enumerate(result):
            if ((i % num_samples) == 0):
                print()
            print('G: {}'.format(' '.join([self.decoder_idx_word[i] for i in pred if (i not in [self.pad, self.eos])])))

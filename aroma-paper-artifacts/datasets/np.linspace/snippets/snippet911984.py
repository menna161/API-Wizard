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


def linear_interpolate_between_inputs(self, checkpoint, start_sent, end_sent, num_samples=8):
    start_sent = word_tokenize(start_sent)
    end_sent = word_tokenize(end_sent)
    start_idx_seq = ([self.decoder_word_index.get(word, self.unk) for word in start_sent] + [self.eos])
    end_idx_seq = ([self.decoder_word_index.get(word, self.unk) for word in end_sent] + [self.eos])
    start_idx_seq = np.concatenate([start_idx_seq, np.zeros(max(0, (self.decoder_num_tokens - len(start_idx_seq))))])[:self.decoder_num_tokens]
    end_idx_seq = np.concatenate([end_idx_seq, np.zeros(max(0, (self.decoder_num_tokens - len(end_idx_seq))))])[:self.decoder_num_tokens]
    inp_idx_seq = np.tile(np.vstack([start_idx_seq, end_idx_seq]), [(self.batch_size // 2), 1])
    z_vecs = self.get_zvector(checkpoint, inp_idx_seq)
    sampled = []
    s1_z = z_vecs[0]
    s2_z = z_vecs[1]
    s1_z = np.repeat(s1_z[(None, :)], num_samples, axis=0)
    s2_z = np.repeat(s2_z[(None, :)], num_samples, axis=0)
    steps = np.linspace(0, 1, num_samples)[(:, None)]
    sampled.append(((s1_z * (1 - steps)) + (s2_z * steps)))
    sampled = np.tile(sampled[0], [(self.batch_size // num_samples), 1])
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess, checkpoint)
        result = sess.run(self.inference_logits, feed_dict={self.z_sampled: sampled, self.keep_prob: 1.0})
        for (i, pred) in enumerate(result[:num_samples]):
            print('G: {}'.format(' '.join([self.decoder_idx_word[i] for i in pred if (i not in [self.pad, self.eos])])))

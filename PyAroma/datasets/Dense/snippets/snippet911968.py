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


def build_decoder(self):
    with tf.variable_scope('decode'):
        for layer in range(self.num_layers):
            with tf.variable_scope('decoder_{}'.format((layer + 1))):
                dec_cell = tf.contrib.rnn.LayerNormBasicLSTMCell((2 * self.lstm_hidden_units))
                dec_cell = tf.contrib.rnn.DropoutWrapper(dec_cell, input_keep_prob=self.keep_prob)
        self.output_layer = Dense(self.decoder_vocab_size)
        self.init_state = dec_cell.zero_state(self.batch_size, tf.float32)
        with tf.name_scope('training_decoder'):
            training_helper = tf.contrib.seq2seq.TrainingHelper(inputs=self.dec_embed_input, sequence_length=self.target_sentence_length, time_major=False)
            training_decoder = basic_decoder.BasicDecoder(dec_cell, training_helper, initial_state=self.init_state, latent_vector=self.z_tilda, output_layer=self.output_layer)
            (self.training_logits, _state, _len) = tf.contrib.seq2seq.dynamic_decode(training_decoder, output_time_major=False, impute_finished=True, maximum_iterations=self.decoder_num_tokens)
            self.training_logits = tf.identity(self.training_logits.rnn_output, 'logits')
        with tf.name_scope('validate_decoder'):
            start_token = self.decoder_word_index['GO']
            end_token = self.decoder_word_index['EOS']
            start_tokens = tf.tile(tf.constant([start_token], dtype=tf.int32), [self.batch_size], name='start_tokens')
            inference_helper = tf.contrib.seq2seq.GreedyEmbeddingHelper(self.decoder_embeddings, start_tokens, end_token)
            inference_decoder = basic_decoder.BasicDecoder(dec_cell, inference_helper, initial_state=self.init_state, latent_vector=self.z_tilda, output_layer=self.output_layer)
            (self.validate_logits, _state, _len) = tf.contrib.seq2seq.dynamic_decode(inference_decoder, output_time_major=False, impute_finished=True, maximum_iterations=self.decoder_num_tokens)
            self.validate_sent = tf.identity(self.validate_logits.sample_id, name='predictions')
        with tf.name_scope('inference_decoder'):
            start_token = self.decoder_word_index['GO']
            end_token = self.decoder_word_index['EOS']
            start_tokens = tf.tile(tf.constant([start_token], dtype=tf.int32), [self.batch_size], name='start_tokens')
            inference_helper = tf.contrib.seq2seq.GreedyEmbeddingHelper(self.decoder_embeddings, start_tokens, end_token)
            inference_decoder = basic_decoder.BasicDecoder(dec_cell, inference_helper, initial_state=self.init_state, latent_vector=self.z_sampled, output_layer=self.output_layer)
            (self.inference_logits, _state, _len) = tf.contrib.seq2seq.dynamic_decode(inference_decoder, output_time_major=False, impute_finished=True, maximum_iterations=self.decoder_num_tokens)
            self.inference_logits = tf.identity(self.inference_logits.sample_id, name='predictions')

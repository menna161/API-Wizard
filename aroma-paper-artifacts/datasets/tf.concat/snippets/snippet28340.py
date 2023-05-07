import tensorflow as tf
import numpy as np
import time
from typing import Dict, Optional, List, Iterable
from collections import Counter
from functools import partial
from path_context_reader import PathContextReader, ModelInputTensorsFormer, ReaderInputTensors, EstimatorAction
from common import common
from vocabularies import VocabType
from config import Config
from model_base import Code2VecModelBase, ModelEvaluationResults, ModelPredictionResults


def _calculate_weighted_contexts(self, tokens_vocab, paths_vocab, attention_param, source_input, path_input, target_input, valid_mask, is_evaluating=False):
    source_word_embed = tf.nn.embedding_lookup(params=tokens_vocab, ids=source_input)
    path_embed = tf.nn.embedding_lookup(params=paths_vocab, ids=path_input)
    target_word_embed = tf.nn.embedding_lookup(params=tokens_vocab, ids=target_input)
    context_embed = tf.concat([source_word_embed, path_embed, target_word_embed], axis=(- 1))
    if (not is_evaluating):
        context_embed = tf.nn.dropout(context_embed, rate=(1 - self.config.DROPOUT_KEEP_RATE))
    flat_embed = tf.reshape(context_embed, [(- 1), self.config.context_vector_size])
    transform_param = tf.compat.v1.get_variable('TRANSFORM', shape=(self.config.context_vector_size, self.config.CODE_VECTOR_SIZE), dtype=tf.float32)
    flat_embed = tf.tanh(tf.matmul(flat_embed, transform_param))
    contexts_weights = tf.matmul(flat_embed, attention_param)
    batched_contexts_weights = tf.reshape(contexts_weights, [(- 1), self.config.MAX_CONTEXTS, 1])
    mask = tf.math.log(valid_mask)
    mask = tf.expand_dims(mask, axis=2)
    batched_contexts_weights += mask
    attention_weights = tf.nn.softmax(batched_contexts_weights, axis=1)
    batched_embed = tf.reshape(flat_embed, shape=[(- 1), self.config.MAX_CONTEXTS, self.config.CODE_VECTOR_SIZE])
    code_vectors = tf.reduce_sum(tf.multiply(batched_embed, attention_weights), axis=1)
    return (code_vectors, attention_weights)

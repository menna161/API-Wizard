import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Input, Embedding, Concatenate, Dropout, TimeDistributed, Dense
from tensorflow.keras.callbacks import Callback
import tensorflow.keras.backend as K
from tensorflow.keras.metrics import sparse_top_k_categorical_accuracy
from path_context_reader import PathContextReader, ModelInputTensorsFormer, ReaderInputTensors, EstimatorAction
import os
import numpy as np
from functools import partial
from typing import List, Optional, Iterable, Union, Callable, Dict
from collections import namedtuple
import time
import datetime
from vocabularies import VocabType
from keras_attention_layer import AttentionLayer
from keras_topk_word_predictions_layer import TopKWordPredictionsLayer
from keras_words_subtoken_metrics import WordsSubtokenPrecisionMetric, WordsSubtokenRecallMetric, WordsSubtokenF1Metric
from config import Config
from common import common
from model_base import Code2VecModelBase, ModelEvaluationResults, ModelPredictionResults
from keras_checkpoint_saver_callback import ModelTrainingStatus, ModelTrainingStatusTrackerCallback, ModelCheckpointSaverCallback, MultiBatchCallback, ModelTrainingProgressLoggerCallback


def perform_evaluation(self):
    if (self.avg_eval_duration is None):
        self.code2vec_model.log('Evaluating...')
    else:
        self.code2vec_model.log('Evaluating... (takes ~{})'.format(str(datetime.timedelta(seconds=int(self.avg_eval_duration)))))
    eval_start_time = time.time()
    evaluation_results = self.code2vec_model.evaluate()
    eval_duration = (time.time() - eval_start_time)
    if (self.avg_eval_duration is None):
        self.avg_eval_duration = eval_duration
    else:
        self.avg_eval_duration = ((eval_duration * 0.5) + (self.avg_eval_duration * 0.5))
    self.code2vec_model.log('Done evaluating (took {}). Evaluation results:'.format(str(datetime.timedelta(seconds=int(eval_duration)))))
    self.code2vec_model.log('    loss: {loss:.4f}, f1: {f1:.4f}, recall: {recall:.4f}, precision: {precision:.4f}'.format(loss=evaluation_results.loss, f1=evaluation_results.subtoken_f1, recall=evaluation_results.subtoken_recall, precision=evaluation_results.subtoken_precision))
    top_k_acc_formated = ['top{}: {:.4f}'.format(i, acc) for (i, acc) in enumerate(evaluation_results.topk_acc, start=1)]
    for top_k_acc_chunk in common.chunks(top_k_acc_formated, 5):
        self.code2vec_model.log(('    ' + ', '.join(top_k_acc_chunk)))

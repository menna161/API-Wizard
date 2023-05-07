import tensorflow as tf
from tensorflow.contrib.seq2seq import BasicDecoder
from tensorflow.contrib.rnn import RNNCell
from tensorflow.contrib.seq2seq import AttentionWrapper
from modules.self_attention import SelfAttention
from modules.rnn_wrappers import RNNStateHistoryWrapper, TransformerWrapper, OutputMgcLf0AndStopTokenWrapper, DecoderMgcLf0PreNetWrapper, OutputAndStopTokenTransparentWrapper, OutputMgcLf0AndStopTokenTransparentWrapper
from modules.helpers import TransformerTrainingHelper, TrainingMgcLf0Helper, ValidationMgcLf0Helper, StopTokenBasedMgcLf0InferenceHelper
from modules.multi_speaker_modules import MultiSpeakerPreNet
from tacotron2.tacotron.modules import PreNet, CBHG, Conv1d, HighwayNet, ZoneoutLSTMCell
from tacotron2.tacotron.tacotron_v1 import DecoderRNNV1
from tacotron2.tacotron.tacotron_v2 import DecoderRNNV2
from tacotron2.tacotron.rnn_wrappers import OutputAndStopTokenWrapper, AttentionRNN, ConcatOutputAndAttentionWrapper, DecoderPreNetWrapper
from tacotron2.tacotron.helpers import StopTokenBasedInferenceHelper, TrainingHelper, ValidationHelper
from tacotron2.tacotron.rnn_impl import LSTMImpl
from functools import reduce
from typing import Tuple


def call(self, inputs, input_lengths=None, **kwargs):
    conv_outputs = tf.concat([conv1d(inputs) for conv1d in self.convolution_banks], axis=(- 1))
    maxpool_output = self.maxpool(conv_outputs)
    proj1_output = self.projection1(maxpool_output)
    proj2_output = self.projection2(proj1_output)
    highway_input = (proj2_output + inputs)
    if (highway_input.shape[2] != (self.out_units // 2)):
        highway_input = self.adjustment_layer(highway_input)
    highway_output = reduce((lambda acc, hw: hw(acc)), self.highway_nets, highway_input)
    (outputs, states) = tf.nn.bidirectional_dynamic_rnn(ZoneoutLSTMCell((self.out_units // 2), self._is_training, zoneout_factor_cell=self._zoneout_factor_cell, zoneout_factor_output=self._zoneout_factor_output, lstm_impl=self._lstm_impl, dtype=self.dtype), ZoneoutLSTMCell((self.out_units // 2), self._is_training, zoneout_factor_cell=self._zoneout_factor_cell, zoneout_factor_output=self._zoneout_factor_output, lstm_impl=self._lstm_impl, dtype=self.dtype), highway_output, sequence_length=input_lengths, dtype=highway_output.dtype)
    return tf.concat(outputs, axis=(- 1))

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


def call(self, inputs, input_lengths=None, positional_encoding=None, **kwargs):
    conv_outputs = tf.concat([conv1d(inputs) for conv1d in self.convolution_banks], axis=(- 1))
    maxpool_output = self.maxpool(conv_outputs)
    proj1_output = self.projection1(maxpool_output)
    proj2_output = self.projection2(proj1_output)
    highway_input = (proj2_output + inputs)
    if (highway_input.shape[2] != (self.out_units // 2)):
        highway_input = self.adjustment_layer(highway_input)
    highway_output = reduce((lambda acc, hw: hw(acc)), self.highway_nets, highway_input)
    self_attention_highway_input = self.self_attention_adjustment_layer(highway_input)
    self_attention_highway_output = reduce((lambda acc, hw: hw(acc)), self.self_attention_highway_nets, self_attention_highway_input)
    self_attention_input = (self_attention_highway_output + positional_encoding)
    (self_attention_output, self_attention_alignments) = self.self_attention(self_attention_input, memory_sequence_length=input_lengths)
    self_attention_output = (self_attention_output + self_attention_highway_output)
    (bilstm_outputs, bilstm_states) = tf.nn.bidirectional_dynamic_rnn(ZoneoutLSTMCell((self.out_units // 2), self._is_training, zoneout_factor_cell=self._zoneout_factor_cell, zoneout_factor_output=self._zoneout_factor_output, dtype=self.dtype), ZoneoutLSTMCell((self.out_units // 2), self._is_training, zoneout_factor_cell=self._zoneout_factor_cell, zoneout_factor_output=self._zoneout_factor_output, dtype=self.dtype), highway_output, sequence_length=input_lengths, dtype=highway_output.dtype)
    bilstm_outputs = tf.concat(bilstm_outputs, axis=(- 1))
    return (bilstm_outputs, self_attention_output, self_attention_alignments)

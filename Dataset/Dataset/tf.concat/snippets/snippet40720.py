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
    (input, accent_type) = inputs
    prenet_output = reduce((lambda acc, pn: pn(acc)), self.prenets, input)
    accent_type_prenet_output = reduce((lambda acc, pn: pn(acc)), self.accent_type_prenets, accent_type)
    concatenated = tf.concat([prenet_output, accent_type_prenet_output], axis=(- 1))
    lstm_output = self.cbhg(concatenated, input_lengths=input_lengths)
    self_attention_input = self.self_attention_projection_layer(lstm_output)

    def self_attend(input, alignments, layer):
        (output, alignment) = layer(input, memory_sequence_length=input_lengths)
        return (output, (alignments + alignment))
    (self_attention_output, self_attention_alignments) = reduce((lambda acc, sa: self_attend(acc[0], acc[1], sa)), self.self_attention, (self_attention_input, []))
    return (lstm_output, self_attention_output, self_attention_alignments)

import numpy as np
import tensorflow as tf
from tensorflow.contrib.seq2seq import BasicDecoder, BahdanauAttention, BahdanauMonotonicAttention, LuongAttention
from tensorflow.contrib.rnn import GRUCell, MultiRNNCell, OutputProjectionWrapper, ResidualWrapper
from utils.infolog import log
from text.symbols import symbols
from .modules import *
from .helpers import TacoTestHelper, TacoTrainingHelper
from .rnn_wrappers import AttentionWrapper, DecoderPrenetWrapper, ConcatOutputAndAttentionWrapper, BahdanauMonotonicAttention_hccho, LocationSensitiveAttention, GmmAttention


def initialize(self, inputs, input_lengths, num_speakers, speaker_id, mel_targets=None, linear_targets=None, loss_coeff=None, rnn_decoder_test_mode=False, is_randomly_initialized=False):
    is_training2 = (linear_targets is not None)
    is_training = (not rnn_decoder_test_mode)
    self.is_randomly_initialized = is_randomly_initialized
    with tf.variable_scope('inference') as scope:
        hp = self._hparams
        batch_size = tf.shape(inputs)[0]
        char_embed_table = tf.get_variable('embedding', [len(symbols), hp.embedding_size], dtype=tf.float32, initializer=tf.truncated_normal_initializer(stddev=0.5))
        zero_pad = True
        if zero_pad:
            char_embed_table = tf.concat((tf.zeros(shape=[1, hp.embedding_size]), char_embed_table[(1:, :)]), 0)
        char_embedded_inputs = tf.nn.embedding_lookup(char_embed_table, inputs)
        self.num_speakers = num_speakers
        if (self.num_speakers > 1):
            if (hp.speaker_embedding_size != 1):
                speaker_embed_table = tf.get_variable('speaker_embedding', [self.num_speakers, hp.speaker_embedding_size], dtype=tf.float32, initializer=tf.truncated_normal_initializer(stddev=0.5))
                speaker_embed = tf.nn.embedding_lookup(speaker_embed_table, speaker_id)
            if (hp.model_type == 'deepvoice'):
                if (hp.speaker_embedding_size == 1):
                    before_highway = get_embed(speaker_id, self.num_speakers, hp.enc_prenet_sizes[(- 1)], 'before_highway')
                    encoder_rnn_init_state = get_embed(speaker_id, self.num_speakers, (hp.enc_rnn_size * 2), 'encoder_rnn_init_state')
                    attention_rnn_init_state = get_embed(speaker_id, self.num_speakers, hp.attention_state_size, 'attention_rnn_init_state')
                    decoder_rnn_init_states = [get_embed(speaker_id, self.num_speakers, hp.dec_rnn_size, 'decoder_rnn_init_states{}'.format((idx + 1))) for idx in range(hp.dec_layer_num)]
                else:
                    deep_dense = (lambda x, dim: tf.layers.dense(x, dim, activation=tf.nn.softsign))
                    before_highway = deep_dense(speaker_embed, hp.enc_prenet_sizes[(- 1)])
                    encoder_rnn_init_state = deep_dense(speaker_embed, (hp.enc_rnn_size * 2))
                    attention_rnn_init_state = deep_dense(speaker_embed, hp.attention_state_size)
                    decoder_rnn_init_states = [deep_dense(speaker_embed, hp.dec_rnn_size) for _ in range(hp.dec_layer_num)]
                speaker_embed = None
            elif (hp.model_type == 'simple'):
                before_highway = None
                encoder_rnn_init_state = None
                attention_rnn_init_state = None
                decoder_rnn_init_states = None
            else:
                raise Exception(' [!] Unkown multi-speaker model type: {}'.format(hp.model_type))
        else:
            speaker_embed = None
            before_highway = None
            encoder_rnn_init_state = None
            attention_rnn_init_state = None
            decoder_rnn_init_states = None
        prenet_outputs = prenet(char_embedded_inputs, is_training, hp.enc_prenet_sizes, hp.dropout_prob, scope='prenet')
        encoder_outputs = cbhg(prenet_outputs, input_lengths, is_training, hp.enc_bank_size, hp.enc_bank_channel_size, hp.enc_maxpool_width, hp.enc_highway_depth, hp.enc_rnn_size, hp.enc_proj_sizes, hp.enc_proj_width, scope='encoder_cbhg', before_highway=before_highway, encoder_rnn_init_state=encoder_rnn_init_state)
        self.is_manual_attention = tf.placeholder(tf.bool, shape=(), name='is_manual_attention')
        self.manual_alignments = tf.placeholder(tf.float32, shape=[None, None, None], name='manual_alignments')
        if (hp.attention_type == 'bah_mon'):
            attention_mechanism = BahdanauMonotonicAttention(hp.attention_size, encoder_outputs, memory_sequence_length=input_lengths, normalize=False)
        elif (hp.attention_type == 'bah_mon_norm'):
            attention_mechanism = BahdanauMonotonicAttention(hp.attention_size, encoder_outputs, memory_sequence_length=input_lengths, normalize=True)
        elif (hp.attention_type == 'loc_sen'):
            attention_mechanism = LocationSensitiveAttention(hp.attention_size, encoder_outputs, memory_sequence_length=input_lengths)
        elif (hp.attention_type == 'gmm'):
            attention_mechanism = GmmAttention(hp.attention_size, memory=encoder_outputs, memory_sequence_length=input_lengths)
        elif (hp.attention_type == 'bah_mon_norm_hccho'):
            attention_mechanism = BahdanauMonotonicAttention_hccho(hp.attention_size, encoder_outputs, normalize=True)
        elif (hp.attention_type == 'bah_norm'):
            attention_mechanism = BahdanauAttention(hp.attention_size, encoder_outputs, memory_sequence_length=input_lengths, normalize=True)
        elif (hp.attention_type == 'luong_scaled'):
            attention_mechanism = LuongAttention(hp.attention_size, encoder_outputs, memory_sequence_length=input_lengths, scale=True)
        elif (hp.attention_type == 'luong'):
            attention_mechanism = LuongAttention(hp.attention_size, encoder_outputs, memory_sequence_length=input_lengths)
        elif (hp.attention_type == 'bah'):
            attention_mechanism = BahdanauAttention(hp.attention_size, encoder_outputs, memory_sequence_length=input_lengths)
        else:
            raise Exception(' [!] Unkown attention type: {}'.format(hp.attention_type))
        attention_cell = AttentionWrapper(GRUCell(hp.attention_state_size), attention_mechanism, self.is_manual_attention, self.manual_alignments, initial_cell_state=attention_rnn_init_state, alignment_history=True, output_attention=False)
        dec_prenet_outputs = DecoderPrenetWrapper(attention_cell, speaker_embed, is_training, hp.dec_prenet_sizes, hp.dropout_prob)
        concat_cell = ConcatOutputAndAttentionWrapper(dec_prenet_outputs, embed_to_concat=speaker_embed)
        cells = [OutputProjectionWrapper(concat_cell, hp.dec_rnn_size)]
        for _ in range(hp.dec_layer_num):
            cells.append(ResidualWrapper(GRUCell(hp.dec_rnn_size)))
        decoder_cell = MultiRNNCell(cells, state_is_tuple=True)
        output_cell = OutputProjectionWrapper(decoder_cell, (hp.num_mels * hp.reduction_factor))
        decoder_init_state = output_cell.zero_state(batch_size=batch_size, dtype=tf.float32)
        if (hp.model_type == 'deepvoice'):
            decoder_init_state = list(decoder_init_state)
            for (idx, cell) in enumerate(decoder_rnn_init_states):
                shape1 = decoder_init_state[(idx + 1)].get_shape().as_list()
                shape2 = cell.get_shape().as_list()
                if (shape1 != shape2):
                    raise Exception(' [!] Shape {} and {} should be equal'.format(shape1, shape2))
                decoder_init_state[(idx + 1)] = cell
            decoder_init_state = tuple(decoder_init_state)
        if is_training2:
            helper = TacoTrainingHelper(inputs, mel_targets, hp.num_mels, hp.reduction_factor, rnn_decoder_test_mode)
        else:
            helper = TacoTestHelper(batch_size, hp.num_mels, hp.reduction_factor)
        ((decoder_outputs, _), final_decoder_state, _) = tf.contrib.seq2seq.dynamic_decode(BasicDecoder(output_cell, helper, decoder_init_state), maximum_iterations=hp.max_iters)
        mel_outputs = tf.reshape(decoder_outputs, [batch_size, (- 1), hp.num_mels])
        post_outputs = cbhg(mel_outputs, None, is_training, hp.post_bank_size, hp.post_bank_channel_size, hp.post_maxpool_width, hp.post_highway_depth, hp.post_rnn_size, hp.post_proj_sizes, hp.post_proj_width, scope='post_cbhg')
        if ((speaker_embed is not None) and (hp.model_type == 'simple')):
            expanded_speaker_emb = tf.expand_dims(speaker_embed, [1])
            tiled_speaker_embedding = tf.tile(expanded_speaker_emb, [1, tf.shape(post_outputs)[1], 1])
            post_outputs = tf.concat([tiled_speaker_embedding, post_outputs], axis=(- 1))
        linear_outputs = tf.layers.dense(post_outputs, hp.num_freq)
        alignments = tf.transpose(final_decoder_state[0].alignment_history.stack(), [1, 2, 0])
        self.inputs = inputs
        self.speaker_id = speaker_id
        self.input_lengths = input_lengths
        self.loss_coeff = loss_coeff
        self.mel_outputs = mel_outputs
        self.linear_outputs = linear_outputs
        self.alignments = alignments
        self.mel_targets = mel_targets
        self.linear_targets = linear_targets
        self.final_decoder_state = final_decoder_state
        log(('=' * 40))
        log((' model_type: %s' % hp.model_type))
        log(('=' * 40))
        log('Initialized Tacotron model. Dimensions: ')
        log(('    embedding:                %d' % char_embedded_inputs.shape[(- 1)]))
        if (speaker_embed is not None):
            log(('    speaker embedding:        %d' % speaker_embed.shape[(- 1)]))
        else:
            log('    speaker embedding:        None')
        log(('    prenet out:               %d' % prenet_outputs.shape[(- 1)]))
        log(('    encoder out:              %d' % encoder_outputs.shape[(- 1)]))
        log(('    attention out:            %d' % attention_cell.output_size))
        log(('    concat attn & out:        %d' % concat_cell.output_size))
        log(('    decoder cell out:         %d' % decoder_cell.output_size))
        log(('    decoder out (%d frames):  %d' % (hp.reduction_factor, decoder_outputs.shape[(- 1)])))
        log(('    decoder out (1 frame):    %d' % mel_outputs.shape[(- 1)]))
        log(('    postnet out:              %d' % post_outputs.shape[(- 1)]))
        log(('    linear out:               %d' % linear_outputs.shape[(- 1)]))

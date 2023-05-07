import io
import os
import re
import librosa
import argparse
import numpy as np
from glob import glob
from tqdm import tqdm
import tensorflow as tf
from functools import partial
from hparams import hparams
from tacotron import create_model, get_most_recent_checkpoint
from utils.audio import save_wav, inv_linear_spectrogram, inv_preemphasis, inv_spectrogram_tensorflow
from utils import plot, PARAMS_NAME, load_json, load_hparams, add_prefix, add_postfix, get_time, parallel_run, makedirs, str2bool
from text.korean import tokenize
from text import text_to_sequence, sequence_to_text
from datasets.datafeeder_tacotron import _prepare_inputs
import warnings


def synthesize(self, texts=None, tokens=None, base_path=None, paths=None, speaker_ids=None, start_of_sentence=None, end_of_sentence=True, pre_word_num=0, post_word_num=0, pre_surplus_idx=0, post_surplus_idx=1, use_short_concat=False, manual_attention_mode=0, base_alignment_path=None, librosa_trim=False, attention_trim=True, isKorean=True):
    if (type(texts) == str):
        texts = [texts]
    if ((texts is not None) and (tokens is None)):
        sequences = np.array([text_to_sequence(text) for text in texts])
        sequences = _prepare_inputs(sequences)
    elif (tokens is not None):
        sequences = tokens
    if (paths is None):
        paths = ([None] * len(sequences))
    if (texts is None):
        texts = ([None] * len(sequences))
    time_str = get_time()

    def plot_and_save_parallel(wavs, alignments, use_manual_attention, mels):
        items = list(enumerate(zip(wavs, alignments, paths, texts, sequences, mels)))
        fn = partial(plot_graph_and_save_audio, base_path=base_path, start_of_sentence=start_of_sentence, end_of_sentence=end_of_sentence, pre_word_num=pre_word_num, post_word_num=post_word_num, pre_surplus_idx=pre_surplus_idx, post_surplus_idx=post_surplus_idx, use_short_concat=use_short_concat, use_manual_attention=use_manual_attention, librosa_trim=librosa_trim, attention_trim=attention_trim, time_str=time_str, isKorean=isKorean)
        return parallel_run(fn, items, desc='plot_graph_and_save_audio', parallel=False)
    input_lengths = [(np.argmax((a == 1)) + 1) for a in sequences]
    fetches = [self.model.linear_outputs, self.model.alignments, self.model.mel_outputs]
    feed_dict = {self.model.inputs: sequences, self.model.input_lengths: input_lengths}
    if (base_alignment_path is None):
        feed_dict.update({self.model.manual_alignments: np.zeros([1, 1, 1]), self.model.is_manual_attention: False})
    else:
        manual_alignments = []
        alignment_path = os.path.join(os.path.basename(base_path), base_alignment_path)
        for idx in range(len(sequences)):
            numpy_path = '{}{}.npy'.format(alignment_path, idx)
            manual_alignments.append(np.load(numpy_path))
        alignments_T = np.transpose(manual_alignments, [0, 2, 1])
        feed_dict.update({self.model.manual_alignments: alignments_T, self.model.is_manual_attention: True})
    if (speaker_ids is not None):
        if (type(speaker_ids) == dict):
            speaker_embed_table = sess.run(self.model.speaker_embed_table)
            speaker_embed = [(speaker_ids[speaker_id] * speaker_embed_table[speaker_id]) for speaker_id in speaker_ids]
            feed_dict.update({self.model.speaker_embed_table: np.tile()})
        else:
            feed_dict[self.model.speaker_id] = speaker_ids
    (wavs, alignments, mels) = self.sess.run(fetches, feed_dict=feed_dict)
    results = plot_and_save_parallel(wavs, alignments, use_manual_attention=False, mels=mels)
    if (manual_attention_mode > 0):
        if (manual_attention_mode == 1):
            alignments_T = np.transpose(alignments, [0, 2, 1])
            new_alignments = np.zeros_like(alignments_T)
            for idx in range(len(alignments)):
                argmax = alignments[idx].argmax(1)
                new_alignments[idx][(argmax, range(len(argmax)))] = 1
        elif (manual_attention_mode == 2):
            new_alignments = np.transpose(alignments, [0, 2, 1])
            for idx in range(len(alignments)):
                var = np.var(new_alignments[idx], 1)
                mean_var = var[:input_lengths[idx]].mean()
                new_alignments[idx] = np.power(new_alignments[idx], 2)
        elif (manual_attention_mode == 3):
            new_alignments = np.transpose(alignments, [0, 2, 1])
            for idx in range(len(alignments)):
                argmax = alignments[idx].argmax(1)
                new_alignments[idx][(argmax, range(len(argmax)))] = 1
        feed_dict.update({self.model.manual_alignments: new_alignments, self.model.is_manual_attention: True})
        (new_wavs, new_alignments) = self.sess.run(fetches, feed_dict=feed_dict)
        results = plot_and_save_parallel(new_wavs, new_alignments, True)
    return results

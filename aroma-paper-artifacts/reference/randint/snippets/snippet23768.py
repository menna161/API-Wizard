import logging
import time
from enum import Enum
import heapq
import numpy as np
import tensorflow.compat.v1 as tf
from rhyme_helper import RhymeWords
import os


def sample_seq(self, session, length, start_text, sample_type=SampleType.max_prob, given='', rhyme_ref='', rhyme_idx=0):
    if (self.cell_type in ['rnn', 'gru']):
        state = self.zero_state.eval()
    else:
        state = tuple([(np.zeros((self.batch_size, self.hidden_size)), np.zeros((self.batch_size, self.hidden_size))) for _ in range(self.num_layers)])
    start_text = self.check_start(start_text)
    if ((start_text is not None) and (len(start_text) > 0)):
        seq = list(start_text)
        for char in start_text[:(- 1)]:
            x = np.array([[self.w2v_model.vocab_hash[char]]])
            state = session.run(self.final_state, {self.input_data: x, self.initial_state: state})
        x = np.array([[self.w2v_model.vocab_hash[start_text[(- 1)]]]])
    else:
        x = np.array([[np.random.randint(0, self.vocab_size)]])
        seq = []
    for i in range(length):
        (state, logits) = session.run([self.final_state, self.logits], {self.input_data: x, self.initial_state: state})
        unnormalized_probs = np.exp((logits[0] - np.max(logits[0])))
        probs = (unnormalized_probs / np.sum(unnormalized_probs))
        if (rhyme_ref and (i == rhyme_idx)):
            sample = self.select_rhyme(rhyme_ref, probs)
        elif (sample_type == SampleType.max_prob):
            sample = np.argmax(probs)
        elif (sample_type == SampleType.select_given):
            (sample, given) = self.select_by_given(given, probs)
        else:
            sample = np.random.choice(self.vocab_size, 1, p=probs)[0]
        seq.append(self.w2v_model.vocab[sample])
        x = np.array([[sample]])
    return ''.join(seq)

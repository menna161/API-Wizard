import torch
import numpy as np
from fairseq.data import data_utils


def noising(self, x, lengths, dropout_prob=None, blank_idx=None):
    if (dropout_prob is None):
        dropout_prob = self.default_dropout_prob
    if (dropout_prob == 0):
        return (x, lengths)
    assert (0 < dropout_prob < 1)
    word_idx = self.get_word_idx(x)
    sentences = []
    modified_lengths = []
    for i in range(lengths.size(0)):
        num_words = (max(word_idx[:, i]) + 1)
        has_eos = (x[((lengths[i] - 1), i)] == self.dictionary.eos())
        if has_eos:
            keep = (np.random.rand((num_words - 1)) >= dropout_prob)
            keep = np.append(keep, [True])
        else:
            keep = (np.random.rand(num_words) >= dropout_prob)
        words = x[:lengths[i], i].tolist()
        new_s = [(w if keep[word_idx[(j, i)]] else blank_idx) for (j, w) in enumerate(words)]
        new_s = [w for w in new_s if (w is not None)]
        if (len(new_s) <= 1):
            new_s.insert(0, words[np.random.randint(0, len(words))])
        assert ((len(new_s) >= 1) and ((not has_eos) or ((len(new_s) >= 2) and (new_s[(- 1)] == self.dictionary.eos())))), 'New sentence is invalid.'
        sentences.append(new_s)
        modified_lengths.append(len(new_s))
    modified_lengths = torch.LongTensor(modified_lengths)
    modified_x = torch.LongTensor(modified_lengths.max(), modified_lengths.size(0)).fill_(self.dictionary.pad())
    for i in range(modified_lengths.size(0)):
        modified_x[:modified_lengths[i], i].copy_(torch.LongTensor(sentences[i]))
    return (modified_x, modified_lengths)

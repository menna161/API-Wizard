import math
import itertools as it
import torch
from fairseq import utils
from examples.speech_recognition.data.replabels import unpack_replabels
from wav2letter.common import create_word_dict, load_words
from wav2letter.criterion import CpuViterbiPath, get_data_ptr_as_bytes
from wav2letter.decoder import CriterionType, DecoderOptions, KenLM, SmearingMode, Trie, WordLMDecoder


def get_tokens(self, idxs):
    'Normalize tokens by handling CTC blank, ASG replabels, etc.'
    idxs = (g[0] for g in it.groupby(idxs))
    idxs = filter((lambda x: (x >= 0)), idxs)
    if (self.criterion_type == CriterionType.CTC):
        idxs = filter((lambda x: (x != self.blank)), idxs)
    elif (self.criterion_type == CriterionType.ASG):
        idxs = unpack_replabels(list(idxs), self.tgt_dict, self.max_replabel)
    return torch.LongTensor(list(idxs))

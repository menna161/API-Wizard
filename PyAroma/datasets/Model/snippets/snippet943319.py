import math
from typing import Dict, List, Optional
import torch
import torch.nn as nn
from fairseq import search, utils
from fairseq.data import data_utils
from fairseq.models import FairseqIncrementalDecoder
from fairseq.models.fairseq_encoder import EncoderOut
from torch import Tensor


def __init__(self, models, tgt_dict, beam_size=1, max_len_a=0, max_len_b=200, min_len=1, normalize_scores=True, len_penalty=1.0, unk_penalty=0.0, temperature=1.0, match_source_len=False, no_repeat_ngram_size=0, search_strategy=None, eos=None):
    'Generates translations of a given source sentence.\n\n        Args:\n            models (List[~fairseq.models.FairseqModel]): ensemble of models,\n                currently support fairseq.models.TransformerModel for scripting\n            beam_size (int, optional): beam width (default: 1)\n            max_len_a/b (int, optional): generate sequences of maximum length\n                ax + b, where x is the source length\n            min_len (int, optional): the minimum length of the generated output\n                (not including end-of-sentence)\n            normalize_scores (bool, optional): normalize scores by the length\n                of the output (default: True)\n            len_penalty (float, optional): length penalty, where <1.0 favors\n                shorter, >1.0 favors longer sentences (default: 1.0)\n            unk_penalty (float, optional): unknown word penalty, where <0\n                produces more unks, >0 produces fewer (default: 0.0)\n            temperature (float, optional): temperature, where values\n                >1.0 produce more uniform samples and values <1.0 produce\n                sharper samples (default: 1.0)\n            match_source_len (bool, optional): outputs should match the source\n                length (default: False)\n        '
    super().__init__()
    if isinstance(models, EnsembleModel):
        self.model = models
    else:
        self.model = EnsembleModel(models)
    self.pad = tgt_dict.pad()
    self.unk = tgt_dict.unk()
    self.eos = (tgt_dict.eos() if (eos is None) else eos)
    self.vocab_size = len(tgt_dict)
    self.beam_size = beam_size
    self.beam_size = min(beam_size, (self.vocab_size - 1))
    self.max_len_a = max_len_a
    self.max_len_b = max_len_b
    self.min_len = min_len
    self.normalize_scores = normalize_scores
    self.len_penalty = len_penalty
    self.unk_penalty = unk_penalty
    self.temperature = temperature
    self.match_source_len = match_source_len
    self.no_repeat_ngram_size = no_repeat_ngram_size
    assert (temperature > 0), '--temperature must be greater than 0'
    self.search = (search.BeamSearch(tgt_dict) if (search_strategy is None) else search_strategy)
    self.should_set_src_lengths = (hasattr(self.search, 'needs_src_lengths') and self.search.needs_src_lengths)
    self.model.eval()

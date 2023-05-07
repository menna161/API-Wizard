from typing import Dict, List, Optional
import torch
import torch.nn as nn
import torch.nn.functional as F
from fairseq import utils
from fairseq.data import Dictionary
from fairseq.models import FairseqDecoder, FairseqEncoder
from fairseq import hub_utils


def __init__(self, encoders, decoders):
    super().__init__()
    assert (encoders.keys() == decoders.keys())
    self.keys = list(encoders.keys())
    for key in self.keys:
        assert isinstance(encoders[key], FairseqEncoder)
        assert isinstance(decoders[key], FairseqDecoder)
    self.models = nn.ModuleDict({key: FairseqModel(encoders[key], decoders[key]) for key in self.keys})

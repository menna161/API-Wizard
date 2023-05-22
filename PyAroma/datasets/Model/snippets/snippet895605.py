import math
import torch
from fairseq import search, utils
from fairseq.data import data_utils
from fairseq.models import FairseqIncrementalDecoder


@torch.no_grad()
def generate(self, models, sample, **kwargs):
    'Generate a batch of translations.\n\n        Args:\n            models (List[~fairseq.models.FairseqModel]): ensemble of models\n            sample (dict): batch\n            prefix_tokens (torch.LongTensor, optional): force decoder to begin\n                with these tokens\n            bos_token (int, optional): beginning of sentence token\n                (default: self.eos)\n        '
    model = EnsembleModel(models)
    return self._generate(model, sample, **kwargs)

import argparse
import tempfile
import unittest
import tests.utils as test_utils
import torch
from fairseq import search
from fairseq.data.dictionary import Dictionary
from fairseq.models.transformer import TransformerModel
from fairseq.sequence_generator import SequenceGenerator, EnsembleModel
from fairseq.tasks.fairseq_task import FairseqTask


@unittest.skipIf((torch.__version__ < '1.6.0'), 'Targeting OSS scriptability for the 1.6 release')
def test_export_ensemble_model(self):
    model = self.transformer_model
    ensemble_models = EnsembleModel([model])
    torch.jit.script(ensemble_models)

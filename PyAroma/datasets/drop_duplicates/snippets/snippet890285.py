from fastai.text import *
from pathlib import Path
import pandas as pd
import numpy as np
import pickle
from .experiment import Labels, label_map
from .ulmfit_experiment import ULMFiTExperiment
import re
from .ulmfit import ULMFiT_SP
from ...pipeline_logger import pipeline_logger
from copy import deepcopy


def __init__(self, path, file, crf_path=None, crf_model=None, sp_path=None, sp_model='spm.model', sp_vocab='spm.vocab'):
    super().__init__(path, file, sp_path, sp_model, sp_vocab)
    self._full_learner = deepcopy(self.learner)
    self.learner.model = cut_ulmfit_head(self.learner.model)
    self.learner.loss_func = None
    if (crf_model is not None):
        crf_path = (Path(path) if (crf_path is None) else Path(crf_path))
        self.crf = load_crf((crf_path / crf_model))
    else:
        self.crf = None
    self._e = ULMFiTExperiment(remove_num=False, drop_duplicates=False, this_paper=True, merge_fragments=True, merge_type='concat', evidence_source='text_highlited', split_btags=True, fixed_tokenizer=True, fixed_this_paper=True, mask=True, evidence_limit=None, context_tokens=None, lowercase=True, drop_mult=0.15, fp16=True, train_on_easy=False)

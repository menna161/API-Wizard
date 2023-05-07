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


def label_tables(self, paper, tables, raw_evidences, in_place=False, use_crf=True):
    pipeline_logger(f'{TableStructurePredictor.step}::label_tables', paper=paper, tables=tables, raw_evidences=raw_evidences)
    if len(raw_evidences):
        tags = self.predict_tags(raw_evidences, use_crf)
        annotations = dict(list(tags.groupby(by=['paper', 'table'])))
    else:
        annotations = {}
    pipeline_logger(f'{TableStructurePredictor.step}::annotations', paper=paper, tables=tables, annotations=annotations)
    labeled = [self.label_table(paper, table, annotations, in_place) for table in tables]
    pipeline_logger(f'{TableStructurePredictor.step}::tables_labeled', paper=paper, labeled_tables=labeled)
    return labeled

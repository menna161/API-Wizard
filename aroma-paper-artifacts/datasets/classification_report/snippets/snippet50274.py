import argparse
import copy
import itertools
import json
import logging
import math
import os
import random
import shutil
import sys
from collections import Counter, defaultdict, OrderedDict
from dataclasses import asdict, dataclass
from os.path import join, dirname, abspath
from typing import Callable, Dict, List, Set, Tuple, Union
import numpy as np
import transformers
import torch
import torch.nn as nn
import torch.nn.functional as F
from dacite import from_dict
from scipy import stats
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from transformers import BertTokenizer
from evidence_inference.preprocess import preprocessor
from evidence_inference.preprocess.preprocessor import PROMPT_ID_COL_NAME, LABEL, EVIDENCE_COL_NAME, EVIDENCE_START, EVIDENCE_END, STUDY_ID_COL
from evidence_inference.preprocess.representations import Document, Sentence, Token, to_structured, retokenize_with_bert
from evidence_inference.models.bert_model import initialize_models


def e2e_score(tru, pred, name, evidence_classes):
    acc = accuracy_score(tru, pred)
    f1 = classification_report(tru, pred, output_dict=False, digits=4, target_names=evidence_classes)
    conf_matrix = confusion_matrix(tru, pred, normalize='true')
    logging.info(f'''{name} classification accuracy {acc},
f1:
{f1}
confusion matrix:
{conf_matrix}
''')

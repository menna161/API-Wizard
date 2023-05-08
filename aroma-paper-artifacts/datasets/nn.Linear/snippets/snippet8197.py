import torch, json, os
from typing import List
from torch import nn
from transformers import BertPreTrainedModel
from transformers.modeling_bert import BertOnlyMLMHead
from torch.nn import CrossEntropyLoss, Linear, Dropout, Module
import gin, logging


def __init__(self, head_task, labels=None, hidden_size=768, hidden_dropout_prob=0.1):
    super(SubwordClassificationHead, self).__init__(type(self).__name__, head_task, labels=labels, hidden_size=hidden_size, hidden_dropout_prob=hidden_dropout_prob)
    self.entity_labels = self.config.labels
    self.config.evaluate_biluo = False
    self.classifier = nn.Linear(hidden_size, len(self.entity_labels))

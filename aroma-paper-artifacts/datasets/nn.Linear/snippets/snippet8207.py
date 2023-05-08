import torch, json, os
from typing import List
from torch import nn
from transformers import BertPreTrainedModel
from transformers.modeling_bert import BertOnlyMLMHead
from torch.nn import CrossEntropyLoss, Linear, Dropout, Module
import gin, logging


def __init__(self, head_task, hidden_size=768, hidden_dropout_prob=0.1, labels=None):
    super(CLSClassificationHead, self).__init__(type(self).__name__, head_task, labels=labels, hidden_size=hidden_size, hidden_dropout_prob=hidden_dropout_prob)
    self.class_labels = self.config.labels
    self.dropout = nn.Dropout(self.config.hidden_dropout_prob)
    self.classifier = nn.Linear(self.config.hidden_size, len(self.class_labels))

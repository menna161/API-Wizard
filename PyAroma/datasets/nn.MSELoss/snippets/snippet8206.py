import torch, json, os
from typing import List
from torch import nn
from transformers import BertPreTrainedModel
from transformers.modeling_bert import BertOnlyMLMHead
from torch.nn import CrossEntropyLoss, Linear, Dropout, Module
import gin, logging


def forward(self, hidden_states: torch.Tensor, attention_mask=None, labels=None, loss_weight=None):
    logits = self.classifier(hidden_states[(:, 0, :)])
    outputs = (logits,)
    if (labels is not None):
        loss_function = torch.nn.MSELoss()
        loss = loss_function(logits.view((- 1)), labels.view((- 1)))
        outputs = ((loss,) + outputs)
    return outputs

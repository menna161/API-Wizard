import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from pytorch_pretrained_bert.modeling import BertModel, BertPreTrainedModel
from torch.nn import CrossEntropyLoss


def __init__(self, config):
    super(BertForQuestionAnswering, self).__init__(config)
    self.bert = BertModel(config)
    self.activation = nn.ReLU()
    self.head_num = 12
    self.mix_lambda = nn.Parameter(torch.tensor(0.5))
    self.linear_q = nn.Linear(config.hidden_size, config.hidden_size, bias=True)
    self.linear_k = nn.Linear(config.hidden_size, config.hidden_size, bias=True)
    self.linear_v = nn.Linear(config.hidden_size, config.hidden_size, bias=True)
    self.linear_o = nn.Linear(config.hidden_size, config.hidden_size, bias=True)
    self.linear_q2 = nn.Linear(config.hidden_size, config.hidden_size, bias=True)
    self.linear_k2 = nn.Linear(config.hidden_size, config.hidden_size, bias=True)
    self.linear_v2 = nn.Linear(config.hidden_size, config.hidden_size, bias=True)
    self.linear_o2 = nn.Linear(config.hidden_size, config.hidden_size, bias=True)
    self.linear_q3 = nn.Linear(config.hidden_size, config.hidden_size, bias=True)
    self.linear_k3 = nn.Linear(config.hidden_size, config.hidden_size, bias=True)
    self.linear_v3 = nn.Linear(config.hidden_size, config.hidden_size, bias=True)
    self.linear_o3 = nn.Linear(config.hidden_size, config.hidden_size, bias=True)
    self.ensemble_linear = nn.Linear(config.hidden_size, config.hidden_size, bias=True)
    self.ensemble_activation = nn.Tanh()
    self.qa_outputs = nn.Linear(config.hidden_size, 2)
    self.apply(self.init_bert_weights)

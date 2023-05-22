import torch.nn as nn
from transformers.modeling_bert import BertPreTrainedModel, BertModel


def __init__(self, config):
    super(BertForMultiLable, self).__init__(config)
    self.bert = BertModel(config)
    self.dropout = nn.Dropout(config.hidden_dropout_prob)
    self.classifier = nn.Linear(config.hidden_size, config.num_labels)
    self.init_weights()

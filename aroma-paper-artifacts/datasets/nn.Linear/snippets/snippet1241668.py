import torch.nn as nn
from .albert.modeling_albert import AlbertPreTrainedModel, AlbertModel


def __init__(self, config):
    super(AlbertForMultiLable, self).__init__(config)
    self.bert = AlbertModel(config)
    self.dropout = nn.Dropout(config.hidden_dropout_prob)
    self.classifier = nn.Linear(config.hidden_size, config.num_labels)
    self.init_weights()

import torch.nn as nn
from transformers.modeling_xlnet import XLNetPreTrainedModel, XLNetModel, SequenceSummary


def __init__(self, config):
    super(XlnetForMultiLable, self).__init__(config)
    self.transformer = XLNetModel(config)
    self.sequence_summary = SequenceSummary(config)
    self.classifier = nn.Linear(config.hidden_size, config.num_labels)
    self.init_weights()

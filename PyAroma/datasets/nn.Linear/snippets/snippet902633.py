import torch
from torch import nn


def __init__(self, config, vocab, device):
    '\n        origin class of the classification model\n        :param config: helper.configure, Configure object\n        :param vocab: data_modules.vocab, Vocab object\n        :param device: torch.device, config.train.device_setting.device\n        '
    super(Classifier, self).__init__()
    self.config = config
    self.device = device
    self.linear = nn.Linear((len(config.text_encoder.CNN.kernel_size) * config.text_encoder.CNN.num_kernel), len(vocab.v2i['label'].keys()))
    self.dropout = nn.Dropout(p=config.model.classifier.dropout)

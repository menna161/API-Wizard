import torch
from torch import nn
from torch.nn import functional
from models.embedding_layer import EmbeddingLayer


def __init__(self, config, label_map, model_mode, graph_model, device):
    "\n        Hierarchy-Aware Global Model : (Parallel) Multi-label attention Variant\n        :param config: helper.configure, Configure Object\n        :param label_map: helper.vocab.Vocab.v2i['label'] -> Dict{str:int}\n        :param model_mode: 'TRAIN'， 'EVAL'\n        :param graph_model: computational graph for graph model\n        :param device: torch.device, config.train.device_setting.device\n        "
    super(HiAGMLA, self).__init__()
    self.config = config
    self.device = device
    self.label_map = label_map
    self.label_embedding = EmbeddingLayer(vocab_map=self.label_map, embedding_dim=config.embedding.label.dimension, vocab_name='label', config=config, padding_index=None, pretrained_dir=None, model_mode=model_mode, initial_type=config.embedding.label.init_type)
    self.graph_model = graph_model
    self.linear = nn.Linear((len(self.label_map) * config.embedding.label.dimension), len(self.label_map))
    self.dropout = nn.Dropout(p=config.model.classifier.dropout)
    self.model_mode = model_mode

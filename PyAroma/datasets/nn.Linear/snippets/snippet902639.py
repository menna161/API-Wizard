import torch
from torch import nn


def __init__(self, config, label_map, graph_model, device):
    "\n        Hierarchy-Aware Global Model : (Serial) Text Propagation Variant\n         :param config: helper.configure, Configure Object\n        :param label_map: helper.vocab.Vocab.v2i['label'] -> Dict{str:int}\n        :param graph_model: computational graph for graph model\n        :param device: torch.device, config.train.device_setting.device\n        "
    super(HiAGMTP, self).__init__()
    self.config = config
    self.device = device
    self.label_map = label_map
    self.graph_model = graph_model
    self.transformation = nn.Linear(config.model.linear_transformation.text_dimension, (len(self.label_map) * config.model.linear_transformation.node_dimension))
    self.linear = nn.Linear((len(self.label_map) * config.embedding.label.dimension), len(self.label_map))
    self.transformation_dropout = nn.Dropout(p=config.model.linear_transformation.dropout)
    self.dropout = nn.Dropout(p=config.model.classifier.dropout)

from __future__ import print_function
import torch
import torch.nn as nn
from types import MethodType
import models
from utils.metric import accuracy, AverageMeter, Timer


def create_model(self):
    cfg = self.config
    model = models.__dict__[cfg['model_type']].__dict__[cfg['model_name']]()
    n_feat = model.last.in_features
    model.last = nn.ModuleDict()
    for (task, out_dim) in cfg['out_dim'].items():
        model.last[task] = nn.Linear(n_feat, out_dim)

    def new_logits(self, x):
        outputs = {}
        for (task, func) in self.last.items():
            outputs[task] = func(x)
        return outputs
    model.logits = MethodType(new_logits, model)
    if (cfg['model_weights'] is not None):
        print('=> Load model weights:', cfg['model_weights'])
        model_state = torch.load(cfg['model_weights'], map_location=(lambda storage, loc: storage))
        model.load_state_dict(model_state)
        print('=> Load Done')
    return model

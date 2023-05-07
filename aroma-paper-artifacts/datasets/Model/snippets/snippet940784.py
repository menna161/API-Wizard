from __future__ import print_function
import os
import sys
import datetime
import torch


def LoadLatestModel(self, model, model_name=None):
    step = 0
    if (len(self.model_lst) == 0):
        print('Empty model folder! Using initial weights')
        return (None, step)
    if (model_name is not None):
        model_name = [x for x in self.model_lst if (('_%s.' % model_name) in x)][0]
    else:
        model_name = self.model_lst[(- 1)]
    print(('Load: %s' % model_name))
    name = ((self.path + '/') + model_name)
    params = torch.load(name)
    model.load_state_dict(params, strict=False)
    strs = model_name.replace('.pkl', '').split('_')
    if (len(strs) == 3):
        step = (int(strs[(- 1)]) + 1)
    return (name, step)

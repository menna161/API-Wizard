from __future__ import print_function
import os
import sys
import datetime
import torch


def Save(self, model, step):
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S_{}'.format(step))
    name = ('%s/model_%s.pkl' % (self.path, now))
    torch.save(model.state_dict(), name)

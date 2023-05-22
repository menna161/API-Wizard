from collections import OrderedDict
import contextlib
from itertools import chain
import math
import os
import sys
import torch
from fairseq import checkpoint_utils, distributed_utils, models, optim, utils
from fairseq.meters import AverageMeter, StopwatchMeter, TimeMeter
from fairseq.optim import lr_scheduler


@property
def model(self):
    if (self._wrapped_model is None):
        if ((self.args.distributed_world_size > 1) and (not self.args.use_bmuf)):
            self._wrapped_model = models.DistributedFairseqModel(self.args, self._model)
        else:
            self._wrapped_model = self._model
    return self._wrapped_model

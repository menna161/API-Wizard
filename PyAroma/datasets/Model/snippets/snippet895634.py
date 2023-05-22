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
def criterion(self):
    if (self._wrapped_criterion is None):
        if (utils.has_parameters(self._criterion) and (self.args.distributed_world_size > 1) and (not self.args.use_bmuf)):
            self._wrapped_criterion = models.DistributedFairseqModel(self.args, self._criterion)
        else:
            self._wrapped_criterion = self._criterion
    return self._wrapped_criterion

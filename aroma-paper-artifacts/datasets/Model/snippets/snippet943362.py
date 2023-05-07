import contextlib
from itertools import chain
import logging
import sys
from typing import Any, Dict, List
import torch
from fairseq import checkpoint_utils, distributed_utils, models, optim, utils
from fairseq.file_io import PathManager
from fairseq.logging import meters, metrics
from fairseq.nan_detector import NanDetector
from fairseq.optim import lr_scheduler
from fairseq import meters
import torch_xla.debug.metrics as met
import torch_xla.core.xla_model as xm
import torch_xla.core.xla_model as xm
import torch_xla.core.xla_model as xm
import torch_xla.core.xla_model as xm
import torch_xla.core.xla_model as xm


@property
def criterion(self):
    if (self._wrapped_criterion is None):
        if (utils.has_parameters(self._criterion) and (self.data_parallel_world_size > 1) and (not self.args.use_bmuf) and (not self.tpu)):
            self._wrapped_criterion = models.DistributedFairseqModel(self.args, self._criterion, process_group=self.data_parallel_process_group)
        else:
            self._wrapped_criterion = self._criterion
    return self._wrapped_criterion
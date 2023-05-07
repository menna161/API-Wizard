from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from collections import defaultdict, OrderedDict
import datetime
import numpy as np
from core.config import cfg
from utils_rel.logging_rel import log_stats
from utils_rel.logging_rel import SmoothedValue
from utils.timer import Timer
import utils.net as nu


def GetStats(self, cur_iter, lr, backbone_lr):
    eta_seconds = (self.iter_timer.average_time * (cfg.SOLVER.MAX_ITER - cur_iter))
    eta = str(datetime.timedelta(seconds=int(eta_seconds)))
    stats = OrderedDict(iter=(cur_iter + 1), time=self.iter_timer.average_time, eta=eta, loss=self.smoothed_total_loss.GetMedianValue(), lr=lr, backbone_lr=backbone_lr)
    stats['metrics'] = OrderedDict()
    for k in sorted(self.smoothed_metrics):
        stats['metrics'][k] = self.smoothed_metrics[k].GetMedianValue()
    head_losses = []
    for (k, v) in self.smoothed_losses.items():
        head_losses.append((k, v.GetMedianValue()))
    stats['head_losses'] = OrderedDict(head_losses)
    return stats

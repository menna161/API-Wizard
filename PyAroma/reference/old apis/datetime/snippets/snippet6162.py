from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime
import numpy as np
from caffe2.python import utils as c2_py_utils
from detectron.core.config import cfg
from detectron.utils.logging import log_json_stats
from detectron.utils.logging import SmoothedValue
from detectron.utils.timer import Timer
import detectron.utils.net as nu


def GetStats(self, cur_iter, lr):
    eta_seconds = (self.iter_timer.average_time * (cfg.SOLVER.MAX_ITER - cur_iter))
    eta = str(datetime.timedelta(seconds=int(eta_seconds)))
    mem_stats = c2_py_utils.GetGPUMemoryUsageStats()
    mem_usage = np.max(mem_stats['max_by_gpu'][:cfg.NUM_GPUS])
    stats = dict(iter=cur_iter, lr=float(lr), time=self.iter_timer.average_time, loss=self.smoothed_total_loss.GetMedianValue(), eta=eta, mb_qsize=int(np.round(self.smoothed_mb_qsize.GetMedianValue())), mem=int(np.ceil(((mem_usage / 1024) / 1024))))
    for (k, v) in self.smoothed_losses_and_metrics.items():
        stats[k] = v.GetMedianValue()
    return stats

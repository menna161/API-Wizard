from ...pipeline_logger import pipeline_logger
import pandas as pd
from enum import Enum


def _filter(self, proposals):
    reason = pd.Series(data='', index=proposals.index)
    indices = []
    if (self.context == 'paper'):
        context_column = proposals.index.to_series().str.split('/', expand=False).apply((lambda x: x[0]))
    else:
        context_column = proposals.index.to_series().str.split('/', expand=False).apply((lambda x: ((x[0] + '/') + x[1])))
    for (key_all, group) in proposals[((proposals.model_type == 'model-best') & (~ proposals.parsed.isna()))].groupby(by=['dataset', 'metric', 'task', context_column]):
        (dataset, metric, task, paper) = key_all
        key = (task, dataset, metric)
        d = 0
        if (key in self.metrics_info):
            d = self.metrics_info[key]
        elif (metric in self.metrics_info):
            d = self.metrics_info[metric]
        elif ('error' in metric.lower()):
            d = (- 1)
        elif ('accuracy' in metric.lower()):
            d = 1
        if (d >= 0):
            index = group.parsed.idxmax()
        else:
            index = group.parsed.idxmin()
        indices.append(index)
        reason[group.index[(group.index != index)]] = ('replaced by ' + str(index))
    reason[(proposals.struct_model_type == 'model-competing')] = 'model-competing'
    which = proposals.index.to_series().isin(indices)
    return (which, reason[(~ which)])

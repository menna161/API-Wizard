import pandas as pd, numpy as np
from dataclasses import dataclass, replace
from axcell.models.linking.metrics import CM
from matplotlib import pyplot as plt
import matplotlib.tri as tri


def sweep_thresholds(df):
    cm = CM(fn=sum(df.gold_positive))
    df = df[(df.min_threshold < df.max_threshold)]
    sweeps = df.reset_index().melt(id_vars='cell_ext_id', value_vars=['min_threshold', 'max_threshold'], var_name='threshold_type', value_name='threshold')
    sweeps = sweeps.sort_values(by=['threshold', 'threshold_type']).reset_index(drop=True)
    steps = sweeps.threshold.drop_duplicates().index
    results = []
    for (i, idx1) in enumerate(steps[:(- 1)]):
        th1 = sweeps.threshold[idx1]
        to_restore = cm
        for (j, idx2) in enumerate(steps[(i + 1):], (i + 1)):
            th2 = sweeps.threshold[idx2]
            precision = (cm.tp / ((cm.tp + cm.fp) + 1e-08))
            recall = (cm.tp / ((cm.tp + cm.fn) + 1e-08))
            f1 = (((2 * precision) * recall) / ((precision + recall) + 1e-08))
            result = dict(threshold1=th1, threshold2=sweeps.threshold[(idx2 - 1)], tp=cm.tp, tn=cm.tn, fp=cm.fp, fn=cm.fn, precision=precision, recall=recall, f1=f1)
            results.append(result)
            for (_, row) in sweeps[(sweeps.threshold == sweeps.threshold[(idx2 - 1)])].iterrows():
                proposal = df.loc[row.cell_ext_id]
                is_activated = (row.threshold_type == 'min_threshold')
                if ((not is_activated) and (proposal.min_threshold < th1)):
                    cm = update_cm(proposal, cm, is_activated)
        precision = (cm.tp / ((cm.tp + cm.fp) + 1e-08))
        recall = (cm.tp / ((cm.tp + cm.fn) + 1e-08))
        f1 = (((2 * precision) * recall) / ((precision + recall) + 1e-08))
        result = dict(threshold1=th1, threshold2=th2, tp=cm.tp, tn=cm.tn, fp=cm.fp, fn=cm.fn, precision=precision, recall=recall, f1=f1)
        results.append(result)
        cm = to_restore
        for (_, row) in sweeps[(sweeps.threshold == th1)].iterrows():
            proposal = df.loc[row.cell_ext_id]
            is_activated = (row.threshold_type == 'min_threshold')
            cm = update_cm(proposal, cm, is_activated)
    return (df, sweeps, steps, pd.DataFrame(results))

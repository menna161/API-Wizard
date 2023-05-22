import re
import pandas as pd
from axcell.data.paper_collection import remove_arxiv_version


def stats(predictions, ground_truth, axis=None):
    gold = pd.DataFrame(ground_truth, columns=['paper', 'task', 'dataset', 'metric', 'value'])
    pred = pd.DataFrame(predictions, columns=['paper', 'task', 'dataset', 'metric', 'value'])
    if (axis == 'tdm'):
        columns = ['paper', 'task', 'dataset', 'metric']
    elif ((axis == 'tdms') or (axis is None)):
        columns = ['paper', 'task', 'dataset', 'metric', 'value']
    else:
        columns = ['paper', axis]
    gold = gold[columns].drop_duplicates()
    pred = pred[columns].drop_duplicates()
    results = gold.merge(pred, on=columns, how='outer', indicator=True)
    is_correct = (results['_merge'] == 'both')
    no_pred = (results['_merge'] == 'left_only')
    no_gold = (results['_merge'] == 'right_only')
    results['TP'] = is_correct.astype('int8')
    results['FP'] = no_gold.astype('int8')
    results['FN'] = no_pred.astype('int8')
    m = results.groupby(['paper']).agg({'TP': 'sum', 'FP': 'sum', 'FN': 'sum'})
    m['precision'] = precision(m.TP, m.FP)
    m['recall'] = recall(m.TP, m.FN)
    m['f1'] = f1(m.precision, m.recall)
    TP_ALL = m.TP.sum()
    FP_ALL = m.FP.sum()
    FN_ALL = m.FN.sum()
    (prec, reca) = (precision(TP_ALL, FP_ALL), recall(TP_ALL, FN_ALL))
    return {'Micro Precision': prec, 'Micro Recall': reca, 'Micro F1': f1(prec, reca), 'Macro Precision': m.precision.mean(), 'Macro Recall': m.recall.mean(), 'Macro F1': m.f1.mean()}

import os
import pickle
import numpy as np
from .util import draw_roc
from .statistic import get_EER_states, get_HTER_at_thr
from sklearn.metrics import roc_auc_score


def eval_metric(results, thr='auto', type='acc', res_dir=None):
    '\n    :param results: np.array shape of (N, 2) [pred, label]\n    :param type: acc acer  or hter\n    :param res_dir: save eval results\n    :return: best score\n    '
    eval_tools = dict(acc=eval_acc, acer=eval_acer, hter=eval_hter)
    results = np.array(results)
    if (type not in ['acc', 'acer', 'hter']):
        raise NotImplementedError
    elif (type == 'hter'):
        eval_score = eval_hter(results, is_print=True)
        return eval_score
    else:
        eval_tool = eval_tools[type]
    if isinstance(thr, float):
        results[(:, 0)] = (results[(:, 0)] > thr).astype(np.float)
        results = results.astype(np.int)
        return eval_tool(results, is_print=True)
    min_score = results[(:, 0)].min()
    max_score = results[(:, 0)].max()
    s_step = ((max_score - min_score) / 1000)
    scores = []
    thrs = []
    for i in range(1000):
        thre = (min_score + (i * s_step))
        thrs.append(thre)
        result = results.copy()
        result[(:, 0)] = (results[(:, 0)] > thre).astype(np.float)
        result = result.astype(np.int)
        score = eval_tool(result, is_print=False)
        scores.append(score)
    max_ind = np.argmax(np.array(scores))
    if (thr == 'mid'):
        sinds = np.argsort(results[(:, 0)])
        best_thr = results[(sinds[(int((results.shape[0] / 2)) - 1)], 0)]
    else:
        best_thr = thrs[max_ind]
    print('Best Threshold: {:.4f}'.format(best_thr))
    save_results = np.zeros((results.shape[0], 3))
    save_results[(:, 2)] = results[(:, 0)]
    results[(:, 0)] = (results[(:, 0)] > best_thr).astype(np.float)
    save_results[(:, :2)] = results[(:, :2)]
    eval_score = eval_tool(results, is_print=True)
    if (res_dir is not None):
        res_dir = os.path.join(res_dir, 'res_{}.pkl'.format(int((eval_score * 10))))
        with open(res_dir, 'wb') as file:
            pickle.dump(save_results, file)
    return eval_score

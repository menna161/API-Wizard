import collections
import inspect
import json
import hashlib
from datetime import datetime
from multiprocessing.pool import Pool
import numpy as np
import pandas as pd
import SimpleITK as sitk
from nnunet.evaluation.metrics import ConfusionMatrix, ALL_METRICS
from batchgenerators.utilities.file_and_folder_operations import save_json, subfiles, join
from collections import OrderedDict


def aggregate_scores_for_experiment(score_file, labels=None, metrics=Evaluator.default_metrics, nanmean=True, json_output_file=None, json_name='', json_description='', json_author='Fabian', json_task=''):
    scores = np.load(score_file)
    scores_mean = scores.mean(0)
    if (labels is None):
        labels = list(map(str, range(scores.shape[1])))
    results = []
    results_mean = OrderedDict()
    for i in range(scores.shape[0]):
        results.append(OrderedDict())
        for (l, label) in enumerate(labels):
            results[(- 1)][label] = OrderedDict()
            results_mean[label] = OrderedDict()
            for (m, metric) in enumerate(metrics):
                results[(- 1)][label][metric] = float(scores[i][l][m])
                results_mean[label][metric] = float(scores_mean[l][m])
    json_dict = OrderedDict()
    json_dict['name'] = json_name
    json_dict['description'] = json_description
    timestamp = datetime.today()
    json_dict['timestamp'] = str(timestamp)
    json_dict['task'] = json_task
    json_dict['author'] = json_author
    json_dict['results'] = {'all': results, 'mean': results_mean}
    json_dict['id'] = hashlib.md5(json.dumps(json_dict).encode('utf-8')).hexdigest()[:12]
    if (json_output_file is not None):
        json_output_file = open(json_output_file, 'w')
        json.dump(json_dict, json_output_file, indent=4, separators=(',', ': '))
        json_output_file.close()
    return json_dict

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


def aggregate_scores(test_ref_pairs, evaluator=NiftiEvaluator, labels=None, nanmean=True, json_output_file=None, json_name='', json_description='', json_author='Fabian', json_task='', num_threads=2, **metric_kwargs):
    '\n    test = predicted image\n    :param test_ref_pairs:\n    :param evaluator:\n    :param labels: must be a dict of int-> str or a list of int\n    :param nanmean:\n    :param json_output_file:\n    :param json_name:\n    :param json_description:\n    :param json_author:\n    :param json_task:\n    :param metric_kwargs:\n    :return:\n    '
    if (type(evaluator) == type):
        evaluator = evaluator()
    if (labels is not None):
        evaluator.set_labels(labels)
    all_scores = OrderedDict()
    all_scores['all'] = []
    all_scores['mean'] = OrderedDict()
    test = [i[0] for i in test_ref_pairs]
    ref = [i[1] for i in test_ref_pairs]
    p = Pool(num_threads)
    all_res = p.map(run_evaluation, zip(test, ref, ([evaluator] * len(ref)), ([metric_kwargs] * len(ref))))
    p.close()
    p.join()
    for i in range(len(all_res)):
        all_scores['all'].append(all_res[i])
        for (label, score_dict) in all_res[i].items():
            if (label in ('test', 'reference')):
                continue
            if (label not in all_scores['mean']):
                all_scores['mean'][label] = OrderedDict()
            for (score, value) in score_dict.items():
                if (score not in all_scores['mean'][label]):
                    all_scores['mean'][label][score] = []
                all_scores['mean'][label][score].append(value)
    for label in all_scores['mean']:
        for score in all_scores['mean'][label]:
            if nanmean:
                all_scores['mean'][label][score] = float(np.nanmean(all_scores['mean'][label][score]))
            else:
                all_scores['mean'][label][score] = float(np.mean(all_scores['mean'][label][score]))
    if (json_output_file is not None):
        json_dict = OrderedDict()
        json_dict['name'] = json_name
        json_dict['description'] = json_description
        timestamp = datetime.today()
        json_dict['timestamp'] = str(timestamp)
        json_dict['task'] = json_task
        json_dict['author'] = json_author
        json_dict['results'] = all_scores
        json_dict['id'] = hashlib.md5(json.dumps(json_dict).encode('utf-8')).hexdigest()[:12]
        save_json(json_dict, json_output_file)
    return all_scores

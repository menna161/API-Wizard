import os, sys, copy, random, torch, numpy as np
from collections import OrderedDict, defaultdict


def get_metrics(self, dataset, setname, iepoch=None, is_random=False):
    x_seeds = self.dataset_seed[dataset]
    results = [self.all_results[(dataset, seed)] for seed in x_seeds]
    infos = defaultdict(list)
    for result in results:
        if (setname == 'train'):
            info = result.get_train(iepoch)
        else:
            info = result.get_eval(setname, iepoch)
        for (key, value) in info.items():
            infos[key].append(value)
    return_info = dict()
    if is_random:
        index = random.randint(0, (len(results) - 1))
        for (key, value) in infos.items():
            return_info[key] = value[index]
    else:
        for (key, value) in infos.items():
            if ((len(value) > 0) and (value[0] is not None)):
                return_info[key] = np.mean(value)
            else:
                return_info[key] = None
    return return_info

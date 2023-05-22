import os
import json
import datetime
import numpy as np
import glob
import framework.configbase


def gen_common_pathcfg(path_cfg_file, is_train=False):
    path_cfg = framework.configbase.PathCfg()
    path_cfg.load(json.load(open(path_cfg_file)))
    output_dir = path_cfg.output_dir
    path_cfg.log_dir = os.path.join(output_dir, 'log')
    path_cfg.model_dir = os.path.join(output_dir, 'model')
    path_cfg.pred_dir = os.path.join(output_dir, 'pred')
    if (not os.path.exists(path_cfg.log_dir)):
        os.makedirs(path_cfg.log_dir)
    if (not os.path.exists(path_cfg.model_dir)):
        os.makedirs(path_cfg.model_dir)
    if (not os.path.exists(path_cfg.pred_dir)):
        os.makedirs(path_cfg.pred_dir)
    if is_train:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        path_cfg.log_file = os.path.join(path_cfg.log_dir, ('log-' + timestamp))
    else:
        path_cfg.log_file = None
    return path_cfg

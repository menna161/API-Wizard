from model_param_space import ModelParamSpace
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials, space_eval
from optparse import OptionParser
from utils import logging_utils, data_utils, embedding_utils, pkl_utils
from utils.eval_utils import strict, loose_macro, loose_micro, label_path, complete_path
import numpy as np
from sklearn.model_selection import ShuffleSplit
import os
import config
import datetime
import tensorflow as tf
from nfetc import NFETC


def main(options):
    time_str = datetime.datetime.now().isoformat()
    logname = ('[Model@%s]_[Data@%s]_%s.log' % (options.model_name, options.data_name, time_str))
    logger = logging_utils._get_logger(config.LOG_DIR, logname)
    optimizer = TaskOptimizer(options.model_name, options.data_name, options.cv_runs, options.max_evals, logger)
    optimizer.run()

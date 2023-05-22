from model_param_space import ModelParamSpace
from hyperopt import fmin, tpe, STATUS_OK, Trials, space_eval
from optparse import OptionParser
from utils import logging_utils, embedding_utils, pkl_utils
import numpy as np
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import average_precision_score
import os
import config
import datetime
import tensorflow as tf
from bilstm import BiLSTM
from complex_hrere import ComplexHRERE
from real_hrere import RealHRERE


def main(options):
    time_str = datetime.datetime.now().isoformat()
    logname = ('[Model@%s]_%s.log' % (options.model_name, time_str))
    logger = logging_utils._get_logger(config.LOG_DIR, logname)
    optimizer = TaskOptimizer(options.model_name, options.max_evals, options.runs, logger)
    optimizer.run()

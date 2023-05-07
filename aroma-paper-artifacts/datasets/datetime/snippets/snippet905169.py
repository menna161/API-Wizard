from optparse import OptionParser
from task import Task
import logging
from utils import logging_utils
from model_param_space import param_space_dict
import datetime
import config


def main(options):
    if options.epoch:
        time_str = datetime.datetime.now().isoformat()
        logname = ('Eval_[Model@%s]_[Data@%s]_%s.log' % (options.model_name, options.data_name, time_str))
        logger = logging_utils._get_logger(config.LOG_DIR, logname)
    else:
        time_str = datetime.datetime.now().isoformat()
        logname = ('Final_[Model@%s]_[Data@%s]_%s.log' % (options.model_name, options.data_name, time_str))
        logger = logging_utils._get_logger(config.LOG_DIR, logname)
    params_dict = param_space_dict[options.model_name]
    task = Task(options.model_name, options.data_name, options.runs, params_dict, logger)
    if options.save:
        task.save()
    elif options.epoch:
        task.refit()
    else:
        task.evaluate(options.full)

import config
from optparse import OptionParser
from task import Task
from utils import logging_utils
from model_param_space import param_space_dict
import datetime


def main(options):
    time_str = datetime.datetime.now().isoformat()
    logname = ('Final_[Model@%s]_%s.log' % (options.model_name, time_str))
    logger = logging_utils._get_logger(config.LOG_DIR, logname)
    params_dict = param_space_dict[options.model_name]
    task = Task(options.model_name, options.runs, params_dict, logger)
    task.evaluate(options.prefix)

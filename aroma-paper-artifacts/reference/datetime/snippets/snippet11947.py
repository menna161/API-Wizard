import json
import numpy as np
import operator
import os
import re
import shutil
import time
from collections import defaultdict
from datetime import datetime
import six
import threading
from ..compat import tfv1 as tf
from ..libinfo import __git_version__
from ..tfutils.summary import create_image_summary, create_scalar_summary
from ..utils import fs, logger
from ..utils.develop import HIDE_DOC
from .base import Callback
from comet_ml import Experiment


def _before_train(self):
    stats = JSONWriter.load_existing_json()
    self._fname = os.path.join(logger.get_logger_dir(), JSONWriter.FILENAME)
    if (stats is not None):
        try:
            epoch = (stats[(- 1)]['epoch_num'] + 1)
        except Exception:
            epoch = None
        starting_epoch = self.trainer.loop.starting_epoch
        if ((epoch is None) or (epoch == starting_epoch)):
            logger.info('Found existing JSON inside {}, will append to it.'.format(logger.get_logger_dir()))
            self._stats = stats
        else:
            logger.warn('History epoch={} from JSON is not the predecessor of the current starting_epoch={}'.format((epoch - 1), starting_epoch))
            logger.warn('If you want to resume old training, either use `AutoResumeTrainConfig` or correctly set the new starting_epoch yourself to avoid inconsistency. ')
            backup_fname = ((JSONWriter.FILENAME + '.') + datetime.now().strftime('%m%d-%H%M%S'))
            backup_fname = os.path.join(logger.get_logger_dir(), backup_fname)
            logger.warn('Now, we will train with starting_epoch={} and backup old json to {}'.format(self.trainer.loop.starting_epoch, backup_fname))
            shutil.move(self._fname, backup_fname)
    self._trigger()

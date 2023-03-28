from __future__ import absolute_import, unicode_literals
import datetime
import imp
import logging
import os
import re
import socket
import traceback
import warnings
from builtins import object, str
from collections import defaultdict
import boto3
import numpy as np
from atm.classifier import Model
from atm.constants import CUSTOM_CLASS_REGEX, SELECTORS, TUNERS
from atm.database import ClassifierStatus, DBSession
from atm.utilities import ensure_directory, get_instance, save_metrics, save_model, update_params


def is_datarun_finished(self):
    '\n        Check to see whether the datarun is finished. This could be due to the\n        budget being exhausted or due to hyperparameter gridding being done.\n        '
    hyperpartitions = self.db.get_hyperpartitions(datarun_id=self.datarun.id)
    if (not hyperpartitions):
        LOGGER.warning(('No incomplete hyperpartitions for datarun %d present in database.' % self.datarun.id))
        return True
    if (self.datarun.budget_type == 'classifier'):
        n_completed = len(self.db.get_classifiers(datarun_id=self.datarun.id))
        if (n_completed >= self.datarun.budget):
            LOGGER.warning('Classifier budget has run out!')
            return True
    elif (self.datarun.budget_type == 'walltime'):
        deadline = self.datarun.deadline
        if (datetime.datetime.now() > deadline):
            LOGGER.warning('Walltime budget has run out!')
            return True
    return False

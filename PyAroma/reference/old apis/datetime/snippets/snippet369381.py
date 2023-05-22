import datetime
import os
import random
import numpy as np
import pytest
from btb.selection import BestKVelocity
from btb.selection.selector import Selector
from btb.tuning import GP
from btb.tuning.tuner import BaseTuner
from mock import ANY, Mock, patch
from atm.classifier import Model
from atm.config import DatasetConfig, RunConfig
from atm.constants import METRICS_BINARY, TIME_FMT
from atm.core import ATM
from atm.database import Database, DBSession
from atm.utilities import load_metrics, load_model
from atm.worker import ClassifierError, Worker


def test_is_datarun_finished(db, dataset, datarun):
    r1 = db.get_datarun(1)
    worker = Worker(db, r1)
    assert worker.is_datarun_finished()
    r2 = db.get_datarun(2)
    worker = Worker(db, r2)
    assert (not worker.is_datarun_finished())
    deadline = (datetime.datetime.now() - datetime.timedelta(seconds=1)).strftime(TIME_FMT)
    worker = get_new_worker(deadline=deadline)
    assert worker.is_datarun_finished()

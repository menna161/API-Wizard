from __future__ import absolute_import
import os
import numpy as np
import contextlib
import datetime
import warnings
import random
import chainer
from chainer.training.extensions._snapshot import _find_latest_snapshot


def get_logstamp(delimiter='_'):
    now = datetime.datetime.now()
    logstamp = []
    logstamp.append(now.strftime('%y%m%d'))
    logstamp.append(now.strftime('%H%M%S'))
    try:
        logstamp.append(get_git_revision())
    except Exception:
        pass
    return delimiter.join(logstamp)

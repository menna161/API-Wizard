import functools
import importlib
import os
import types
from collections import defaultdict
from datetime import datetime
import six
from . import logger
import inspect


def log_deprecated(name='', text='', eos='', max_num_warnings=None):
    '\n    Log deprecation warning.\n\n    Args:\n        name (str): name of the deprecated item.\n        text (str, optional): information about the deprecation.\n        eos (str, optional): end of service date such as "YYYY-MM-DD".\n        max_num_warnings (int, optional): the maximum number of times to print this warning\n    '
    assert (name or text)
    if eos:
        eos = ('after ' + datetime(*map(int, eos.split('-'))).strftime('%d %b'))
    if name:
        if eos:
            warn_msg = ('%s will be deprecated %s. %s' % (name, eos, text))
        else:
            warn_msg = ('%s was deprecated. %s' % (name, text))
    else:
        warn_msg = text
        if eos:
            warn_msg += (' Legacy period ends %s' % eos)
    if (max_num_warnings is not None):
        if (_DEPRECATED_LOG_NUM[warn_msg] >= max_num_warnings):
            return
        _DEPRECATED_LOG_NUM[warn_msg] += 1
    logger.warn(('[Deprecated] ' + warn_msg))

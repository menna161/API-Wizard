import uuid
import datetime as dt
from functools import reduce
import logging
import inspect
from .io import Input, Output, get_if_exists
from .errors import PyungoError
from .utils import get_function_return_names
from .data import Data
import jsonschema
from multiprocess import Pool


def __call__(self, *args, **kwargs):
    ' run the function attached to the node, and store the result '
    t1 = dt.datetime.utcnow()
    res = self._fct(*args, **kwargs)
    t2 = dt.datetime.utcnow()
    LOGGER.info('Ran {} in {}'.format(self, (t2 - t1)))
    if (len(self._outputs) == 1):
        self._outputs[0].value = res
    else:
        for (i, out) in enumerate(self._outputs):
            out.value = res[i]
    return res

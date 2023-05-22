import inspect
import types
from collections import defaultdict
from datetime import datetime
from enum import Enum
from typing import Callable
from flask import jsonify, request, url_for
from werkzeug.datastructures import MultiDict, ImmutableMultiDict
from appkernel.http_client import RequestHandlingException
from .configuration import config
from .core import AppKernelException
from .engine import AppKernelEngine
from .iam import RbacMixin, Denied
from .model import Model, PropertyRequiredException, get_argument_spec, OPS, tag_class_items
from .query import QueryProcessor
from .reflection import is_noncomplex, is_primitive, is_dictionary, is_dictionary_subclass
from .repository import xtract, Repository
from .util import create_custom_error
from .validators import ValidationException
import simplejson as json
import json


def _remap_expressions(expression):
    "\n    Takes a query expression such as >1994-12-02 and turns into a {'$gte':'1994-12-02'}.\n    Additionally converts the date string into datetime object;\n\n    :param expression:\n    :return:\n    "
    if (expression[0] in qp.supported_expressions):
        converted_value = _convert_expressions(expression[1:])
        return qp.expression_mapper.get(expression[0])(converted_value)
    else:
        return _convert_expressions(expression)

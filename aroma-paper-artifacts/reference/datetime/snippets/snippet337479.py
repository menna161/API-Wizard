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


def _convert_expressions(expression):
    '\n    converts strings containing numbers to int, string containing a date to datetime, string containing a boolean expression to boolean\n\n    :param arguments:\n    :return:\n    '
    if isinstance(expression, str):
        if qp.number_pattern.match(expression):
            return int(expression)
        if qp.boolean_pattern.match(expression):
            return (True if (expression in ['true', 'True', 'y', 'yes']) else False)
        for date_pattern in qp.date_patterns.keys():
            if date_pattern.match(expression):
                for parser_format_matcher in qp.date_separator_patterns.keys():
                    if parser_format_matcher.match(expression):
                        date_parser_pattern = qp.date_patterns.get(date_pattern)
                        separator = qp.date_separator_patterns.get(parser_format_matcher)
                        return datetime.strptime(expression, date_parser_pattern.format(separator))
    return expression

from typing import Callable
import collections
import inspect
from datetime import datetime, date
from enum import Enum
from bson import ObjectId
from flask_babel import lazy_gettext
from .core import AppKernelException
from .validators import Validator, NotEmpty, Unique, Max, Min, Regexp, Email
from .util import default_json_serializer, OBJ_PREFIX
import simplejson as json
import json


def __init__(self, python_type, required: bool=False, sub_type: Callable=None, validators: Callable=None, converter: Callable=None, default_value: Callable=None, generator: Callable=None, index: Index=None, marshaller: Callable=None, omit=False) -> ():
    "\n        Args:\n            python_type(type): the primary python type of the attribute (eg. str, datetime or anything else);\n            required(bool): if True, the field must be specified before validation;\n            sub_type(type): in case the python type is a dict or a list (or any other collection type), one needs to specify the element types\n            validators(Validator): a list of validator elements which are used to validate field content\n            converter: converts the value of the property in the finalisation phase (before generating a json or saving in the database). Useful to hash passwords or encrypt custom content;\n            default_value(object): this value is set on the field in case there's no other value there yet\n            generator(function): content generator, perfect for date.now() generation or for field values calculated from other fields (eg. signatures)\n            index(Index): the type of index (if any) which needs to be added to the database;\n            marshaller(Marshaller):\n            omit(bool): if True, the field won't be included in the json or other wire-format messages\n        "
    self.omit = omit
    self.index = index
    self.python_type = python_type
    self.required = required
    self.sub_type = sub_type
    self.validators = validators
    self.converter = converter
    self.default_value = default_value
    self.marshaller = marshaller
    self.generator = generator

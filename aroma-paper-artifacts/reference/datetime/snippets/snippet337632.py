import datetime
import re
from enum import Enum
from flask_babel import _
from .model import AppKernelException


def validate(self, parameter_name, validable_object):
    if (validable_object is None):
        return
    elif (not self._is_date(validable_object)):
        raise ValidationException(f'The parameter {parameter_name} is none or not date type.', validable_object, self.type)
    elif (validable_object >= datetime.datetime.now()):
        raise ValidationException(f'The parameter {parameter_name} must define the past.', validable_object, self.type)

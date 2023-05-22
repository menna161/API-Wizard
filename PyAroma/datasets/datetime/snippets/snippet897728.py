import os
import json
import uuid
import logging
import datetime
from collections import defaultdict, OrderedDict
import jsonschema
from jsonschema import Draft3Validator, FormatChecker
import scrapelib
from pupa import utils
from pupa import settings
from pupa.exceptions import ScrapeError, ScrapeValueError


def validate(self, schema=None):
    "\n        Validate that we have a valid object.\n\n        On error, this will raise a `ScrapeValueError`\n\n        This also expects that the schemas assume that omitting required\n        in the schema asserts the field is optional, not required. This is\n        due to upstream schemas being in JSON Schema v3, and not validictory's\n        modified syntax.\n        ^ TODO: FIXME\n        "
    if (schema is None):
        schema = self._schema
    type_checker = Draft3Validator.TYPE_CHECKER.redefine('datetime', (lambda c, d: isinstance(d, (datetime.date, datetime.datetime))))
    type_checker = type_checker.redefine('date', (lambda c, d: (isinstance(d, datetime.date) and (not isinstance(d, datetime.datetime)))))
    ValidatorCls = jsonschema.validators.extend(Draft3Validator, type_checker=type_checker)
    validator = ValidatorCls(schema, format_checker=FormatChecker())
    errors = [str(error) for error in validator.iter_errors(self.as_dict())]
    if errors:
        raise ScrapeValueError('validation of {} {} failed: {}'.format(self.__class__.__name__, self._id, ('\n\t' + '\n\t'.join(errors))))

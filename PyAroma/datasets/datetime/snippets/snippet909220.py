import datetime
import re
from typing import Any


def validate(self, val):
    super().validate(val)
    if (val is None):
        return
    if (not isinstance(val, datetime.datetime)):
        raise ValidationError

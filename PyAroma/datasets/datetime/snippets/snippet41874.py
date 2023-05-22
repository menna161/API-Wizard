from datetime import date, datetime, timedelta, tzinfo
from typing import Callable, Optional, Union
from django.conf import settings
from django.utils import timezone
from faker import Faker


def past_datetime(start='-30d'):
    "\n    Returns a ``datetime`` object in the past between 1 second ago and the\n    specified ``start``. ``start`` can be a string, another datetime, or a\n    timedelta. If it's a string, it must start with `-`, followed by and integer\n    and a unit, Eg: ``'-30d'``. Defaults to `'-30d'`\n\n    Valid units are:\n    * ``'years'``, ``'y'``\n    * ``'weeks'``, ``'w'``\n    * ``'days'``, ``'d'``\n    * ``'hours'``, ``'h'``\n    * ``'minutes'``, ``'m'``\n    * ``'seconds'``, ``'s'``\n    "
    return (lambda n, f: f.past_datetime(start_date=start, tzinfo=get_timezone()))

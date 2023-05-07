from datetime import date, datetime, timedelta, tzinfo
from typing import Callable, Optional, Union
from django.conf import settings
from django.utils import timezone
from faker import Faker


def future_datetime(end='+30d'):
    "\n    Returns a ``datetime`` object in the future (that is, 1 second from now) up\n    to the specified ``end``. ``end`` can be a string, another datetime, or a\n    timedelta. If it's a string, it must start with `+`, followed by and integer\n    and a unit, Eg: ``'+30d'``. Defaults to `'+30d'`\n\n    Valid units are:\n    * ``'years'``, ``'y'``\n    * ``'weeks'``, ``'w'``\n    * ``'days'``, ``'d'``\n    * ``'hours'``, ``'hours'``\n    * ``'minutes'``, ``'m'``\n    * ``'seconds'``, ``'s'``\n    "
    return (lambda n, f: f.future_datetime(end_date=end, tzinfo=get_timezone()))

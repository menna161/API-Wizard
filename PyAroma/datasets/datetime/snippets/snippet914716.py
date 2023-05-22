from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone
import datetime
from django.forms import ValidationError
import traceback
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings as main_settings
from . import settings
from . import views
from .views import get_today_now
import importlib as imp
from django.core.management import call_command
from django.core.management.base import CommandError
from freezegun import freeze_time
from .models import Customer, Treatment, Resource, Entry
from django.contrib.auth.models import User


def yearsago(years, from_date=None):
    '\n    Workaround for datetime.timedelta not knowing how to calculate leap years.\n    Adapted from:\n    http://stackoverflow.com/questions/765797/python-timedelta-in-years\n    '
    if (from_date is None):
        from_date = timezone.now()
    try:
        return from_date.replace(year=(from_date.year - years))
    except:
        assert ((from_date.month == 2) and (from_date.day == 29))
        return from_date.replace(month=2, day=28, year=(from_date.year - years))

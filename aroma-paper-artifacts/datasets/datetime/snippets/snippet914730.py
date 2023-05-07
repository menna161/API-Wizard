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


def test_entry_equality_identity(self):
    '\n        Entries with identical dates, times and durations are equal.\n        '
    dateDelta1 = datetime.timedelta(days=0)
    time1 = datetime.time(hour=12)
    duration1 = datetime.timedelta(hours=1)
    entry1 = create_entry_from_delta(dateDelta1, time1, duration1, 'time calc test 1')
    dateDelta2 = datetime.timedelta(days=0)
    time2 = datetime.time(hour=12)
    duration2 = datetime.timedelta(hours=1)
    entry2 = create_entry_from_delta(dateDelta2, time2, duration2, 'time calc test 1')
    self.assertTrue((entry1 == entry2))

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


@freeze_time('2015-10-12 12:00:00')
def test_entry_customer_in_past(self):
    "\n        Make sure customers cannot book in the past.\n\n        This test is patched to provide a constant value of 'now'\n        "
    customer = create_customer('test')
    dateDelta = datetime.timedelta(days=0)
    date = timezone.localtime(timezone.now()).date()
    now = timezone.localtime(timezone.now()).time()
    time = change_time(date, now, datetime.timedelta(hours=(- 1)))
    duration = datetime.timedelta(hours=1)
    entry = create_entry_from_delta(dateDelta, time, duration, 'past test 1')
    entry.editor = customer
    self.assertRaisesMessage(ValidationError, 'Please book a date/time in the future.', entry.clean)

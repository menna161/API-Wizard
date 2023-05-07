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
def test_entry_staff_out_of_hours(self):
    '\n        Make sure staff are able to book any time.\n\n        This test is patched to avoid complications with changing times.\n        '
    dateDelta = datetime.timedelta(days=14)
    date = datetime.datetime.today().date()
    openingTime = settings.DIARY_OPENING_TIMES[date.weekday()]
    time1 = change_time(date, openingTime, datetime.timedelta(hours=(- 1)))
    duration = datetime.timedelta(hours=1)
    entry = create_entry_from_delta(dateDelta, time1, duration, 'trading hours test 2')
    try:
        entry.clean()
        self.assertTrue((entry == entry))
    except Exception as e:
        traceback.print_exc()
        self.fail('Cleaning an entry with no conflicts \nraised an unexpected exception: \n{0}'.format(e))

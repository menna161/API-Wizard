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


def test_cancelled_entry_resource_clash_clean_no_exception(self):
    '\n        Make sure cleaning the data raises no Exception when the entry is\n        cancelled even with a resource clash.\n        '
    resource = create_resource('resource', 'resource')
    dateDelta1 = datetime.timedelta(days=0)
    time1 = datetime.time(hour=12)
    duration1 = datetime.timedelta(hours=1)
    entry1 = create_entry_from_delta(dateDelta1, time1, duration1, 'time calc test 1')
    entry1.resource = resource
    entry1.save()
    dateDelta2 = datetime.timedelta(days=0)
    time2 = datetime.time(hour=12)
    duration2 = datetime.timedelta(hours=1)
    entry2 = create_entry_from_delta(dateDelta2, time2, duration2, 'time calc test 1')
    entry2.resource = resource
    entry2.cancelled = True
    try:
        entry2.clean()
        self.assertTrue((entry1 == entry2))
    except Exception as e:
        traceback.print_exc()
        self.fail('Cleaning a cancelled entry with \na time clash raised an unexpected exception: \n{0}'.format(e))

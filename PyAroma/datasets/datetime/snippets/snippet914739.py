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


def test_entry_resource_clash_no_resource_means_no_clash(self):
    '\n        Entries using no resources do not generate any conflicts even when they\n        overlap in time.\n        '
    dateDelta1 = datetime.timedelta(days=0)
    time = datetime.time(hour=12)
    duration = datetime.timedelta(hours=1)
    entry1 = create_entry_from_delta(dateDelta1, time, duration, 'resource_conflict_test_entry_1')
    entry1.save()
    dateDelta2 = datetime.timedelta(days=0)
    entry2 = create_entry_from_delta(dateDelta2, time, duration, 'resource_conflict_test_entry_2')
    try:
        entry2.clean()
        self.assertTrue((entry1 == entry2))
    except Exception as e:
        traceback.print_exc()
        self.fail('Cleaning an entry with no resources \nraised an unexpected exception: \n{0}'.format(e))

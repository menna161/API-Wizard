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


def test_entry_treatment_resource_required(self):
    '\n        If the entry has a treatment that specifies a resource a resource must\n        be defined.\n        '
    entry = create_entry_from_delta(datetime.timedelta(days=0), datetime.time(hour=12), datetime.timedelta(hours=0), 'resource_required_test')
    try:
        entry.clean()
        self.assertFalse((entry is None))
    except Exception as e:
        traceback.print_exc()
        self.fail('Cleaning an entry with no treatment raised an unexpected exception: \n{0}'.format(e))
    entry.treatment = create_treatment('requires_resource', datetime.timedelta(hours=1), True)
    self.assertRaisesMessage(ValidationError, 'Resource requirement is not met.', entry.clean)
    entry.resource = create_resource('resource', 'resource')
    self.assertRaisesMessage(ValidationError, 'Duration must be at least the minimum treament time.', entry.clean)
    entry.duration = datetime.time(hour=1)
    try:
        entry.clean()
        self.assertFalse((entry is None))
    except Exception as e:
        traceback.print_exc()
        self.fail('Cleaning an entry with\ntreatment resource and duration raised an unexpected exception: \n{0}'.format(e))

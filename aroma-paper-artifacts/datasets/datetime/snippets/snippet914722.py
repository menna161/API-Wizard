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


def create_entry_from_delta(dateDelta, time, duration, notes):
    '\n    Utility to create an entry for testing using a dateDelta.\n    '
    date = (timezone.datetime.today() + dateDelta)
    return create_entry(date, time, duration, notes)

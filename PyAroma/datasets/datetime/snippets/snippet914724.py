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


def create_entries():
    tenYearsAgo = yearsago(10)
    fiveYearsAgo = yearsago(5)
    now = yearsago(0)
    time = datetime.time(hour=12)
    duration = datetime.timedelta(hours=1)
    entry1 = create_entry(tenYearsAgo, time, duration, 'very old entry')
    entry1.save()
    entry2 = create_entry(fiveYearsAgo, time, duration, 'old entry')
    entry2.save()
    entry3 = create_entry(now, time, duration, 'new')
    entry3.save()

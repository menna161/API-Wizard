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


def create_customer(username):
    '\n    Utility to generate a customer\n    '
    customer = Customer.objects.create_user(username, username, username, (username + '@example.com'), '123456', datetime.date(year=1950, month=6, day=1), 'M', 'test user')
    customer.save()
    return customer

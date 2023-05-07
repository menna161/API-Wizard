from django.db import models
from django.contrib import admin
import datetime
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import User, UserManager
from django.forms import ValidationError
from . import settings


def time_end(self):
    '\n        Calculate the time of the end of the entry from the start time and the\n        duration.\n        Sadly the naive method of adding the duration directly to the time\n        is not supported in python datetime arithmetic; a datetime object has\n        to be used.\n        '
    the_time = datetime.datetime.combine(self.date, self.time)
    the_time_end = (the_time + self.duration_delta())
    return the_time_end.time()

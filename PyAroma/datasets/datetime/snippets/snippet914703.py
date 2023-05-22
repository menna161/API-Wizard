from django.db import models
from django.contrib import admin
import datetime
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import User, UserManager
from django.forms import ValidationError
from . import settings


def duration_delta(self):
    '\n        Convert duration-as-time to duration-as-delta.\n        '
    the_zero = datetime.datetime.combine(self.date, DURATION_ZERO)
    the_duration = datetime.datetime.combine(self.date, self.duration)
    return (the_duration - the_zero)

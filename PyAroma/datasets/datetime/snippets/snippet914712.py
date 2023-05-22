from django.db import models
from django.contrib import admin
import datetime
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import User, UserManager
from django.forms import ValidationError
from . import settings


def validateFuture(self):
    '\n        Ensure customers cannot book times in the past or in the advance booking\n        period.\n\n        Staff can book entries whenever they like, but customers can only book\n        times in the future.\n        '
    if (not self.editor.is_staff):
        tz_now = timezone.localtime(timezone.now())
        now = datetime.datetime(tz_now.year, tz_now.month, tz_now.day, tz_now.hour, tz_now.minute, tz_now.second)
        advance_booking_date = (datetime.datetime(tz_now.year, tz_now.month, tz_now.day, 0, 0, 0) + datetime.timedelta(days=settings.DIARY_MIN_BOOKING))
        bookedTime = datetime.datetime.combine(self.date, self.time)
        if (bookedTime < now):
            raise ValidationError('Please book a date/time in the future.')
        if (bookedTime < advance_booking_date):
            raise ValidationError('Need to book ahead.')

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
import datetime
from django.utils import timezone
import calendar
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.db.models import Q
from django.forms import ValidationError
from django.template.loader import render_to_string
from django.template import RequestContext
from .models import Entry, Customer
from .forms import EntryForm
from .admin import CustomerCreationForm, CustomerChangeForm
from . import settings


def evaluateBusinessLogic(day, startTime, endTime):
    '\n    Evaluate the booleans that control the display business logic for day and\n    multi-day views.\n    '
    (today, now) = get_today_now()
    current = (((now >= startTime) and (now < endTime)) and (day == today))
    trading = ((startTime >= settings.DIARY_OPENING_TIMES[day.weekday()]) and (endTime <= settings.DIARY_CLOSING_TIMES[day.weekday()]))
    historic = ((day < today) or ((day == today) and (endTime < now)))
    booking_allowed_date = (today + datetime.timedelta(days=settings.DIARY_MIN_BOOKING))
    before_advance = (day < booking_allowed_date)
    allow_dnd = (trading and (not (historic or before_advance)))
    return (current, trading, historic, before_advance, allow_dnd)

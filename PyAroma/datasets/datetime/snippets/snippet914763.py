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


def getDate(year, month, day, change):
    '\n    Helper function to obtain the date from kwargs.\n    '
    print('DEPRECATED:  Getting kwargs date...')
    (today, now) = get_today_now()
    if (not year):
        (year, month, day) = (today.year, today.month, today.day)
    else:
        (year, month, day) = (int(year), int(month), int(day))
    date = timezone.datetime(year=year, month=month, day=day).date()
    if change:
        dayDelta = datetime.timedelta(days=1)
        if (change == 'prev'):
            dayDelta = datetime.timedelta(days=(- 1))
        date = (date + dayDelta)
    return date

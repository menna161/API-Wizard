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


def getDateFromSlug(slug, change):
    '\n    Helper to derive a date from an iso format slug.\n    '
    (today, now) = get_today_now()
    date = None
    if (not slug):
        date = today
    else:
        date = datetime.datetime.strptime(slug, DATE_SLUG_FORMAT).date()
    if change:
        dayDelta = datetime.timedelta(days=1)
        if (change == 'prev'):
            dayDelta = datetime.timedelta(days=(- 1))
        date = (date + dayDelta)
    return date

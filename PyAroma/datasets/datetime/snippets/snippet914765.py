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


def getDatetimeFromSlug(slug):
    '\n    Helper method to derive a date and time from a datetime slug.\n    '
    date_time = datetime.datetime.strptime(slug, DATETIME_SLUG_FORMAT)
    return (date_time.date(), date_time.time())

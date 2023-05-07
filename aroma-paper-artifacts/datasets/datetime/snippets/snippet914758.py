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


def evaluateTimeSlots():
    '\n    Calculate labels and starting times for diary day display.\n    Returns a list of labels and start/end times of time slots.\n    '
    DUMMY_DAY = timezone.localtime(timezone.now()).date()
    time = datetime.datetime.combine(DUMMY_DAY, settings.DIARY_MIN_TIME)
    finish = datetime.datetime.combine(DUMMY_DAY, settings.DIARY_MAX_TIME)
    timeSlots = []
    while (time <= finish):
        thisTime = time.time()
        time += settings.DIARY_TIME_INC
        timeSlots.append((thisTime.strftime(TIME_FORMAT), thisTime.strftime(TIME_SLUG_FORMAT), thisTime, time.time()))
    return timeSlots

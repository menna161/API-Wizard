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


@login_required
def multi_day(request, slug=None, change=None):
    '\n    Display entries in a calendar-style 4-day layout.\n    '
    date = getDateFromSlug(slug, change)
    date_slots = []
    dayDelta = datetime.timedelta(days=1)
    for i in range(0, settings.DIARY_MULTI_DAY_NUMBER):
        day = (date + (i * dayDelta))
        dayHeader = day.strftime('%a %d')
        date_slug = day.strftime(DATE_SLUG_FORMAT)
        date_slots.append((day, dayHeader, date_slug))
    date_start_head = date_slots[0][0].strftime('%b %d')
    date_end_head = date_slots[(- 1)][0].strftime('%b %d')
    nav_slug = date_slots[0][0].strftime(DATE_SLUG_FORMAT)
    time_slots = []
    for (timeLabel, time_slug, startTime, endTime) in TIME_SLOTS:
        day_entries = []
        for (day, dayHeader, date_slug) in date_slots:
            entries = (Entry.objects.filter(date=day, time__gte=startTime, time__lt=endTime) if request.user.is_staff else Entry.objects.filter(date=day, time__gte=startTime, time__lt=endTime, customer=request.user, cancelled=False)).order_by('time')
            (current, trading_time, historic, before_advance, allow_dnd) = evaluateBusinessLogic(day, startTime, endTime)
            day_entries.append(('_'.join((date_slug, time_slug)), entries, current, trading_time, historic, before_advance, allow_dnd))
        time_slots.append((timeLabel, startTime, day_entries))
    return render(request, 'diary/multi_day.html', {'date': date, 'n_cols': settings.DIARY_MULTI_DAY_NUMBER, 'date_start_head': date_start_head, 'date_end_head': date_end_head, 'nav_slug': nav_slug, 'user': request.user, 'month_name': MONTH_NAMES[(date.month - 1)], 'time_slots': time_slots, 'date_slots': date_slots, 'reminders': reminders(request)})

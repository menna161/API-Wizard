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
def month(request, year=None, month=None, change=None):
    '\n    Display the days in the specified month.\n    '
    (today, now) = get_today_now()
    if (not year):
        (year, month) = (today.year, today.month)
    else:
        (year, month) = (int(year), int(month))
    date = timezone.datetime(year=year, month=month, day=15).date()
    if change:
        monthDelta = datetime.timedelta(days=31)
        if (change == 'prev'):
            monthDelta = datetime.timedelta(days=(- 31))
        date = (date + monthDelta)
    cal = calendar.Calendar(calendar.firstweekday())
    month_days = cal.itermonthdays(date.year, date.month)
    weeks = [[]]
    week_no = 0
    for day in month_days:
        entry_list = statistics = current = None
        nav_slug = None
        if day:
            dayDate = datetime.date(year=date.year, month=date.month, day=day)
            entries = (Entry.objects.filter(date=dayDate) if request.user.is_staff else Entry.objects.filter(date=dayDate, customer=request.user, cancelled=False))
            if request.user.is_staff:
                statistics = get_statistics(entries)
            else:
                entry_list = list(entries)
            nav_slug = dayDate.strftime(DATE_SLUG_FORMAT)
            current = (dayDate == today)
        weeks[week_no].append((day, nav_slug, entry_list, statistics, current))
        if (len(weeks[week_no]) == 7):
            weeks.append([])
            week_no += 1
    return render(request, 'diary/month.html', {'date': date, 'weeks': weeks, 'month_name': MONTH_NAMES[(date.month - 1)], 'day_names': DAY_NAMES, 'reminders': reminders(request)})

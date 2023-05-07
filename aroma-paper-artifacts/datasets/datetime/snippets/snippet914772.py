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
def entry_modal(request, pk):
    '\n    Prepare and send an html snippet to display an entry in a modal dialog via\n    ajax - but using html.\n    '
    redirect_url = request.GET.get('redirect_url', reverse('diary:day_now'))
    entry = get_object_or_404(Entry, pk=pk)
    (today, now) = get_today_now()
    enable_edit_buttons = False
    enable_no_show_button = False
    enable_history_button = (not ('history' in redirect_url))
    book_ahead_date = (entry.date + datetime.timedelta(days=7))
    book_ahead_datetime_slug = datetime.datetime.combine(book_ahead_date, entry.time).strftime(DATETIME_SLUG_FORMAT)
    if request.user.is_staff:
        enable_edit_buttons = True
        enable_no_show_button = ((not entry.no_show) and ((entry.date < today) or ((entry.date == today) and (entry.time < now))))
    else:
        booking_threshold = (today + datetime.timedelta(days=settings.DIARY_MIN_BOOKING))
        if ((entry.date == today) and (booking_threshold == today) and (entry.time > now)):
            enable_edit_buttons = True
        elif ((booking_threshold > today) and (entry.date >= booking_threshold)):
            enable_edit_buttons = True
    html = render_to_string('diary/modal_entry.html', context={'entry': entry, 'redirect_url': redirect_url, 'enable_edit_buttons': enable_edit_buttons, 'enable_no_show_button': enable_no_show_button, 'enable_history_button': enable_history_button, 'book_ahead_datetime_slug': book_ahead_datetime_slug}, request=request)
    return HttpResponse(html)

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


def reminders(request):
    '\n    Data for the reminder sidebar.\n    '
    (today, now) = get_today_now()
    tomorrow = (today + datetime.timedelta(days=1))
    user = request.user
    queryset = (Entry.objects.filter((Q(date=today, time__gte=now) | Q(date=tomorrow)), customer=user, cancelled=False) if isinstance(user, Customer) else Entry.objects.filter((Q(date=today, time__gte=now) | Q(date=tomorrow))))
    return queryset.order_by('date', 'time')

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
def entry_update(request):
    "\n    Update an entry's details via ajax.\n    At present only the date and time can be changed this way.\n    "
    pk = request.POST['pk']
    entry = get_object_or_404(Entry, pk=pk)
    entry.editor = request.user
    datetime_slug = request.POST['slug']
    (date, time) = getDatetimeFromSlug(datetime_slug)
    entry.date = date
    entry.time = time
    entry.no_show = False
    entry.cancelled = False
    try:
        entry.save()
    except ValidationError as ve:
        endTime = (datetime.datetime.combine(date, time) + DIARY_TIME_INC).time()
        otherEntry = Entry.objects.filter(date=date, time__gte=time, time__lt=endTime).first()
        if (otherEntry.time_end() >= endTime):
            raise ve
        entry.time = otherEntry.time_end()
        entry.save()
    message = 'Date / time changed to {0}, {1}'.format(entry.date, entry.time)
    data = {'message': message}
    return JsonResponse(data)

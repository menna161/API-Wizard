from decimal import Decimal
import datetime
from datetime import timedelta
import json
import re
import smtplib
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotAllowed
from django.db import transaction, IntegrityError
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Event, Grant, Comment, User, FreeResponseQuestion, EligibilityQuestion, Item, CATEGORIES, CommonFollowupQuestion, FollowupQuestion, CommonFreeResponseQuestion, CFAUser
from .forms import EventForm
from django.db.models import Q


@require_http_methods(['GET', 'POST'])
def events(request):
    if (not request.user.is_authenticated):
        return LoginView.as_view()(request)
    user = request.user
    sorted_type = (request.GET.get('sort').strip() if ('sort' in request.GET) else 'date')
    query_dict = {'event': 'name', 'org': 'organizations', 'submit': '-updated_at'}
    sort_by = (query_dict[sorted_type] if (sorted_type in query_dict) else '-date')
    cfauser = user.profile
    status_val = request.GET.get('status', '')
    filter_val = request.GET.get('filter', '')
    app = Event.objects.all()
    if (user.is_staff and (not (user.username == 'uacontingency'))):
        app = app
    elif cfauser.is_requester:
        app = app.filter(requester=cfauser)
    else:
        app = app.exclude(status='S')
        app = cfauser.event_applied_funders.order_by(sort_by)
    if (len(status_val) != 0):
        if (status_val == 'O'):
            app = app.filter(date__lt=(datetime.date.today() - timedelta(days=14)))
        else:
            app = app.filter(date__gte=(datetime.date.today() - timedelta(days=14)))
            app = app.filter(status__in=status_val)
    app = app.filter((Q(name__icontains=filter_val) | Q(organizations__icontains=filter_val)))
    app = app.order_by(sort_by)
    if ('page' in request.GET):
        page = request.GET['page']
    else:
        page = 1
    p = Paginator(app, 10)
    return render(request, 'app/events.html', {'apps': p.page(page).object_list, 'page_obj': p.page(page), 'page_range': p.page_range, 'page_length': len(p.page_range), 'status': status_val})

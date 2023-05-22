import datetime
import itertools
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError, models, transaction
from . import signals


def fetch_top_objects(model, time_limit):
    queryset = model.objects.all()
    if (time_limit is None):
        if issubclass(model, get_user_model()):
            queryset = queryset.annotate(num_points=models.Sum('targetstat_targets__points'))
        else:
            raise NotImplementedError('Only auth.User is supported at this time.')
    else:
        since = (datetime.datetime.now() - time_limit)
        if issubclass(model, get_user_model()):
            queryset = queryset.filter(awardedpointvalue_targets__timestamp__gte=since).annotate(num_points=models.Sum('awardedpointvalue_targets__points'))
        else:
            raise NotImplementedError('Only auth.User is supported at this time.')
    queryset = queryset.filter(num_points__isnull=False).order_by('-num_points')
    return queryset

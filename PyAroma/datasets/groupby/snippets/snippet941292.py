import datetime
import itertools
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError, models, transaction
from . import signals


@classmethod
def update_positions(cls, point_range=None):
    queryset = cls._default_manager.order_by('-points')
    if (point_range is not None):
        if (point_range[0] > point_range[1]):
            point_range = (point_range[1], point_range[0])
        all_target_stats = queryset.filter(points__range=point_range)
        position = queryset.filter(points__gt=point_range[1]).count()
    else:
        all_target_stats = queryset
        position = 0
    grouped_target_stats = itertools.groupby(all_target_stats, (lambda x: x.points))
    prev_group_len = 0
    for (points, target_stats) in grouped_target_stats:
        position += (prev_group_len + 1)
        target_stats = list(target_stats)
        prev_group_len = (len(target_stats) - 1)
        pks = []
        for target_stat in target_stats:
            pks.append(target_stat.pk)
        cls._default_manager.filter(pk__in=pks).update(position=position)

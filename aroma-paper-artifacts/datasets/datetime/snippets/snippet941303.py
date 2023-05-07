import datetime
from django import template
from django.apps import apps
from ..models import fetch_top_objects, points_awarded


def __init__(self, model, context_var, limit, time_num, time_unit):
    self.model = template.Variable(model)
    self.context_var = context_var
    if (limit is None):
        self.limit = None
    else:
        self.limit = template.Variable(limit)
    if ((time_num is None) or (time_unit is None)):
        self.time_limit = None
    else:
        self.time_limit = datetime.timedelta(**{time_unit: int(time_num)})

import datetime
from django import template
from django.apps import apps
from ..models import fetch_top_objects, points_awarded


def render(self, context):
    obj = self.obj.resolve(context)
    since = None
    if ((self.limit_num is not None) and (self.limit_unit is not None)):
        since = (datetime.datetime.now() - datetime.timedelta(**{self.limit_unit: int(self.limit_num)}))
    points = points_awarded(obj, since=since)
    if (self.context_var is not None):
        context[self.context_var] = points
        return ''
    return str(points)

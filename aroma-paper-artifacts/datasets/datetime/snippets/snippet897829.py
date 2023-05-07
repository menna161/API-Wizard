import sys
from datetime import datetime, timezone, timedelta
import django
from django.apps import apps
from .base import BaseCommand
from opencivicdata.core.models.base import OCDBase


def get_stale_objects(self, window):
    "\n        Find all database objects that haven't seen been in {window} days.\n        "
    from opencivicdata.core.models.base import OCDBase
    ocd_apps = ['core', 'legislative']
    models = get_subclasses(ocd_apps, OCDBase)
    for model in models:
        if ('Jurisdiction' not in model.__name__):
            cutoff_date = (datetime.now(tz=timezone.utc) - timedelta(days=window))
            (yield from model.objects.filter(last_seen__lte=cutoff_date).iterator())

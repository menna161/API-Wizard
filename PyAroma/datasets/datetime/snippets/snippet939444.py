from datetime import datetime, timedelta
from mongoengine import *
from celery import current_app
import celery.schedules


def save(self, force_insert=False, validate=True, clean=True, write_concern=None, cascade=None, cascade_kwargs=None, _refs=None, save_condition=None, signal_kwargs=None, **kwargs):
    if (not self.date_creation):
        self.date_creation = datetime.now()
    self.date_changed = datetime.now()
    super(PeriodicTask, self).save(force_insert, validate, clean, write_concern, cascade, cascade_kwargs, _refs, save_condition, signal_kwargs, **kwargs)

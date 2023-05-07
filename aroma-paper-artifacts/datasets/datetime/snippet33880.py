import json
import uuid
import calendar
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from jsonfield import JSONField


@property
def timestamp(self):
    'UTC timestamp of self.created datetime.datetime field'
    return calendar.timegm(self.created.utctimetuple())

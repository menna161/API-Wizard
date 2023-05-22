import os
import json
import pytz
import datetime
import subprocess


def default(self, obj, **kwargs):
    if isinstance(obj, datetime.datetime):
        if (obj.tzinfo is None):
            raise TypeError(("date '%s' is not fully timezone qualified." % obj))
        obj = obj.astimezone(pytz.UTC)
        return '{}'.format(obj.isoformat())
    elif isinstance(obj, datetime.date):
        return '{}'.format(obj.isoformat())
    return super(JSONEncoderPlus, self).default(obj, **kwargs)

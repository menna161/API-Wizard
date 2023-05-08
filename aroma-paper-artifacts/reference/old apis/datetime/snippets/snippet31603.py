from __future__ import absolute_import
import datetime
import uuid
from googleapiclient import errors
from oauth2client import util
import six


@util.positional(2)
def new_webhook_channel(url, token=None, expiration=None, params=None):
    'Create a new webhook Channel.\n\n    Args:\n      url: str, URL to post notifications to.\n      token: str, An arbitrary string associated with the channel that\n        is delivered to the target address with each notification delivered\n        over this channel.\n      expiration: datetime.datetime, A time in the future when the channel\n        should expire. Can also be None if the subscription should use the\n        default expiration. Note that different services may have different\n        limits on how long a subscription lasts. Check the response from the\n        watch() method to see the value the service has set for an expiration\n        time.\n      params: dict, Extra parameters to pass on channel creation. Currently\n        not used for webhook channels.\n    '
    expiration_ms = 0
    if expiration:
        delta = (expiration - EPOCH)
        expiration_ms = ((delta.microseconds / 1000) + ((delta.seconds + ((delta.days * 24) * 3600)) * 1000))
        if (expiration_ms < 0):
            expiration_ms = 0
    return Channel('web_hook', str(uuid.uuid4()), token, url, expiration=expiration_ms, params=params)

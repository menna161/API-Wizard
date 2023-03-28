import logging
import re
import json
from webapp2 import *
from webapp2_extras.routes import DomainRoute
from datetime import datetime, timedelta
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import memcache
import cloudstorage


def should_update(self):
    'Tests to see if the last check was long enough past the update interval\n    that we should update the version.'
    return (datetime.now() > (self.last_check + self.update_interval))

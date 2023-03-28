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


def recheck_latest_version(self, channel):
    'Check Google storage to determine the latest version file in a given\n    channel.'
    data = None
    version_file_location = self.version_file_loc(channel)
    with cloudstorage.open(version_file_location, 'r') as f:
        line = f.readline()
        data = line.replace('\x00', '')
        ApiDocs.latest_versions[channel].last_check = datetime.now()
    revision = data
    ApiDocs.latest_versions[channel].version = revision
    return revision

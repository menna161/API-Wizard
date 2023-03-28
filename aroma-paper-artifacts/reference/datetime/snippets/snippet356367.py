from __future__ import with_statement
import calendar
import datetime
import email
import logging
import mimetypes
import os
import stat
import subprocess
import tornado.web
import assetman


def set_expires_header(self):
    if self.expires:
        expires_at = (datetime.datetime.utcnow() + datetime.timedelta(days=(365 * 10)))
        max_age = ((86400 * 365) * 10)
        self.set_header('Expires', expires_at)
        self.set_header('Cache-Control', ('public, max-age=%s' % max_age))
    else:
        self.set_header('Cache-Control', 'no-cache')

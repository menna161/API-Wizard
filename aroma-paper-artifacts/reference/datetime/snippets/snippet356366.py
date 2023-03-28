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


def get(self, path, include_body=True):
    abs_path = os.path.normpath(os.path.join(self.root, path))
    if ((not os.path.isfile(abs_path)) or (not abs_path.startswith(self.root))):
        raise tornado.web.HTTPError(404, 'File %s not found', path)
    stat_result = os.stat(abs_path)
    modified = datetime.datetime.utcfromtimestamp(stat_result[stat.ST_MTIME])
    self.set_header('Last-Modified', modified)
    self.set_expires_header()
    self.set_mime_type(abs_path)
    ims_value = self.request.headers.get('If-Modified-Since')
    if (ims_value is not None):
        date_tuple = email.utils.parsedate(ims_value)
        if_since = datetime.datetime.utcfromtimestamp(calendar.timegm(date_tuple))
        if (if_since >= modified):
            logging.debug('Not modified since %s', if_since)
            self.set_status(304)
            return
    if (not include_body):
        return
    self.set_header('Content-Length', stat_result[stat.ST_SIZE])
    with open(abs_path, 'rb') as f:
        logging.debug('Response headers: %r', self._headers)
        self.write(f.read())

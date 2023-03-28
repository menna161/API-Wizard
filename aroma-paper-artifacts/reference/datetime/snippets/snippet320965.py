import argparse
import logging
import os
import sys
from copy import deepcopy
from datetime import datetime
from aminator.util import randword
import bunch
from pkg_resources import resource_string, resource_exists
import aminator
from logging.config import dictConfig
from yaml import CLoader as Loader
from logutils.dictconfig import dictConfig
from yaml import Loader


def configure_datetime_logfile(config, handler):
    try:
        filename_format = config.logging[handler]['filename_format']
    except KeyError:
        log.error('filename_format not configured for handler {0}'.format(handler))
        return
    try:
        pkg = '{0}-{1}'.format(os.path.basename(config.context.package.arg), randword(6))
        filename = os.path.join(config.log_root, filename_format.format(pkg, datetime.utcnow()))
    except IndexError:
        errstr = 'Missing replacement fields in filename_format for handler {0}'.format(handler)
        log.error(errstr)
        log.debug(errstr, exc_info=True)
    for h in ([x for l in logging.root.manager.loggerDict for x in logging.getLogger(l).handlers] + logging.root.handlers):
        if (getattr(h, 'name', '') == handler):
            assert isinstance(h, logging.FileHandler)
            h.stream.close()
            h.baseFilename = filename
            h.stream = open(filename, 'a')
            url_template = config.logging[handler].get('web_log_url_template', False)
            if url_template:
                url_attrs = config.context.web_log.toDict()
                url_attrs['logfile'] = os.path.basename(filename)
                url = url_template.format(**url_attrs)
                log.info('Detailed {0} output to {1}'.format(handler, url))
            else:
                log.info('Detailed {0} output to {1}'.format(handler, filename))
            break
    else:
        log.error('{0} handler not found.'.format(handler))

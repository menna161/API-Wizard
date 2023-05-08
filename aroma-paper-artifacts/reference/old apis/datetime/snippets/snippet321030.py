import logging
from datetime import datetime
import abc
from os import environ
from aminator.config import conf_action
from aminator.exceptions import FinalizerException
from aminator.plugins.finalizer.base import BaseFinalizerPlugin


def _add_tags(self, resources):
    context = self._config.context
    context.ami.tags.creation_time = '{0:%F %T UTC}'.format(datetime.utcnow())
    for resource in resources:
        try:
            self._cloud.add_tags(resource)
        except FinalizerException:
            errstr = 'Error adding tags to {0}'.format(resource)
            log.error(errstr)
            log.debug(errstr, exc_info=True)
            return False
        log.info('Successfully tagged {0}'.format(resource))
    log.info('Successfully tagged objects')
    return True

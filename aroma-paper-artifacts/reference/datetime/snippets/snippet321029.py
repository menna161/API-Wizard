import logging
from datetime import datetime
import abc
from os import environ
from aminator.config import conf_action
from aminator.exceptions import FinalizerException
from aminator.plugins.finalizer.base import BaseFinalizerPlugin


def _set_metadata(self):
    context = self._config.context
    config = self._config.plugins[self.full_name]
    log.debug('Populating snapshot and ami metadata for tagging and naming')
    creator = context.ami.get('creator', config.get('creator', 'aminator'))
    context.ami.tags.creator = creator
    context.snapshot.tags.creator = creator
    metadata = context.package.attributes
    metadata['arch'] = context.base_ami.architecture
    metadata['base_ami_name'] = context.base_ami.name
    metadata['base_ami_id'] = context.base_ami.id
    metadata['base_ami_version'] = context.base_ami.tags.get('base_ami_version', '')
    suffix = context.ami.get('suffix', None)
    if (not suffix):
        suffix = config.suffix_format.format(datetime.utcnow())
    metadata['suffix'] = suffix
    for tag in config.tag_formats:
        try:
            context.ami.tags[tag] = config.tag_formats[tag].format(**metadata)
            context.snapshot.tags[tag] = config.tag_formats[tag].format(**metadata)
        except KeyError as e:
            errstr = 'Tag format requires information not available in package metadata: {0}'.format(e.message)
            log.warn(errstr)
            log.debug(errstr, exc_info=True)
            continue
    default_description = config.description_format.format(**metadata)
    description = context.snapshot.get('description', default_description)
    context.ami.description = description
    context.snapshot.description = description

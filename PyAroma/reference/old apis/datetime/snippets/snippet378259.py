from __future__ import absolute_import, print_function, unicode_literals, with_statement
import croniter
import datetime
import logging
import os
import threading
import salt.returners
import salt.utils
from cloud_cache import prepare_result_recursively
from common_util import jsonl_dump, makedirs, RotatingTextFile
from threading_more import AsyncWriterThread, on_exit
from timeit import default_timer as timer


def _get_writer_for(ret):
    writer = getattr(tlocal, 'writer', None)
    if ((not writer) or writer.closed):
        with tlock:
            options = _get_options(ret)
            key = options['filename'].format(now=EPOC_DATETIME, uid=__opts__['id'], pid=os.getpid(), tid=threading.currentThread().ident)
            writer = __context__.setdefault('cloud_jsonl_returner.writers', {}).get(key, None)
            if ((not writer) or writer.closed):

                def open_file(obj):
                    now = datetime.datetime.utcnow()
                    format_kwargs = dict(now=now, uid=__opts__['id'], pid=os.getpid(), tid=threading.currentThread().ident)
                    directory = options['dir'].format(**format_kwargs)
                    filename = options['filename'].format(**format_kwargs)
                    obj.max_size = options['rotation.size']
                    expiration_times = []
                    if (options['rotation.interval'] > 0):
                        expiration_times.append(float((now + datetime.timedelta(seconds=options['rotation.interval'])).strftime('%s')))
                    if options['rotation.cron']:
                        expiration_times.append(float(croniter.croniter(options['rotation.cron'], now).get_next()))
                    obj.expiration_time = (min(expiration_times) if expiration_times else 0)
                    makedirs(directory, exist_ok=True)
                    log.info("Opening JSONL file '{:}'".format(filename))
                    return open(os.path.join(directory, filename), 'a', buffering=0)
                writer = AsyncWriterThread(RotatingTextFile(open_file), **{k[len('async_writer.'):]: v for (k, v) in options.iteritems() if k.startswith('async_writer.')})
                __context__['cloud_jsonl_returner.writers'][key] = writer
            elif DEBUG:
                log.debug('Re-using writer {:} found in context'.format(writer))
        setattr(tlocal, 'writer', writer)
    elif DEBUG:
        log.debug('Re-using writer {:} found in thread local'.format(writer))
    return writer

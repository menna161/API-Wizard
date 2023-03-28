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


def set_expiration(delay, reason='unknown'):
    '\n    Set or clear expiration for this returner.\n    Delay of zero means instant expiration.\n    Negative delay will clear any already set expiration.\n    '
    with tlock:
        ctx = __context__.setdefault('cloud_jsonl_returner.expiration', {})
        if (delay < 0):
            if ctx:
                if is_expired():
                    close_writers()
                ctx.clear()
                log.info("Cleared expiration with reason '{:}'".format(reason))
            else:
                log.info("Attempted to clear expiration with reason '{:}' but no expiration is set".format(reason))
        elif is_expired():
            log.info("Already expired with reason '{:}'".format(ctx.get('reason', '')))
        else:
            if (delay > 0):
                ctx['time'] = float((datetime.datetime.now() + datetime.timedelta(seconds=delay)).strftime('%s'))
            else:
                ctx['time'] = 0
            ctx['reason'] = reason
            log.info("Set expiration to {:} with reason '{:}'".format(ctx['time'], ctx['reason']))
        return ctx

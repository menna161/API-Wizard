import copy
import datetime
import logging
import re
import salt.exceptions
import salt.utils.event
import threading
import threading_more
import time
import urlparse
import uuid
from common_util import ensure_primitive, last_iter
from salt_more import cached_loader, SuperiorCommandExecutionError
from timeit import default_timer as timer


def do_work(thread, context):
    success = True
    for message in list(context['messages']):
        try:
            self._call_hook_for(message, 'workflow', message)
        except Warning as wa:
            success = False
            context['last_warning'] = datetime.datetime.utcnow().isoformat()
            msg = str(wa)
            context.setdefault('distinct_warnings', {}).setdefault(msg, 0)
            context['distinct_warnings'][msg] += 1
            if ((context['distinct_warnings'][msg] > 3) and ((timer() - getattr(thread, 'warning_log_timer', 0)) < 60)):
                return
            setattr(thread, 'warning_log_timer', timer())
            if (context['distinct_warnings'][msg] > 1):
                log.info("Recurring warning ({:} times) in worker thread '{:}': {:}".format(context['distinct_warnings'][msg], thread.name, wa))
            else:
                log.info("Warning in worker thread '{:}': {:}".format(thread.name, wa))
        except Exception as ex:
            success = False
            context['last_error'] = datetime.datetime.utcnow().isoformat()
            msg = str(ex)
            context.setdefault('distinct_errors', {}).setdefault(msg, 0)
            context['distinct_errors'][msg] += 1
            if (suppress_exceptions and (context['distinct_errors'][msg] > 3) and ((timer() - getattr(thread, 'exception_log_timer', 0)) < 60)):
                return
            setattr(thread, 'exception_log_timer', timer())
            if (context['distinct_errors'][msg] > 1):
                log.exception("Recurring exception ({:} times) in worker thread '{:}' while running workflow for message: {:}".format(context['distinct_errors'][msg], thread.name, message))
            else:
                log.exception("Exception in worker thread '{:}' while running workflow for message: {:}".format(thread.name, message))
            if suppress_exceptions:
                if transactional:
                    log.info("Suppressing prior exception in worker thread '{:}' and skips any following work".format(thread.name))
                    break
                else:
                    log.info("Suppressing prior exception in worker thread '{:}' and continues as normal".format(thread.name))
            else:
                raise
    if success:
        context.pop('distinct_warnings', None)
        context.pop('distinct_errors', None)
    if (kill_upon_success and success):
        thread.kill()
        if DEBUG:
            log.debug("Killed worker thread '{:}' upon successful run".format(thread.name))

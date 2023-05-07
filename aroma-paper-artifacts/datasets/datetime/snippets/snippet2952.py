import datetime
import logging
from weakref import WeakKeyDictionary
from nameko.extensions import DependencyProvider


def worker_result(self, worker_ctx, result=None, exc_info=None):
    service_name = worker_ctx.service_name
    method_name = worker_ctx.entrypoint.method_name
    status = ('completed' if (exc_info is None) else 'errored')
    now = datetime.datetime.now()
    worker_started = self.timestamps.pop(worker_ctx)
    if (self.interval == 's'):
        duration = (now - worker_started).seconds
    elif (self.interval == 'ms'):
        duration = (now - worker_started).microseconds
    msg = 'Worker {service}.{method} {status} after {duration}{interval}'.format(service=service_name, method=method_name, status=status, duration=duration, interval=self.interval)
    logging.info(msg)

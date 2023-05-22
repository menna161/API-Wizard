import datetime
import logging
from weakref import WeakKeyDictionary
from nameko.extensions import DependencyProvider


def worker_setup(self, worker_ctx):
    self.timestamps[worker_ctx] = datetime.datetime.now()
    service_name = worker_ctx.service_name
    method_name = worker_ctx.entrypoint.method_name
    logging.info('Worker {service}.{method} starting'.format(service=service_name, method=method_name))

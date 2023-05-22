import datetime
import gzip
import json
import logging
import random
import re
import redis
import requests
import StringIO
import time
from requests.exceptions import RequestException
from timeit import default_timer as timer


def upload_pending(self):
    ret = {'total': 0}
    try:
        res = self._upload_batch_continuing(self.PENDING_QUEUE)
        ret['total'] += res['count']
        if ('error' in res):
            ret.setdefault('errors', []).append(res['error'])
    except RequestException as rex:
        ret.setdefault('errors', []).append(str(rex))
        work_queue = self.WORK_QUEUE.format(self.PENDING_QUEUE)
        if (self.options.get('max_retry', 10) > 0):
            retry_queue = self.RETRY_QUEUE.format(datetime.datetime.utcnow(), 0)
            log.warning("Failed to upload pending batch - transferring to new dedicated retry queue '{:}': {:}".format(retry_queue, rex))
            self.client.pipeline().renamenx(work_queue, retry_queue).bgsave().execute()
        else:
            log.warning("Failed to upload pending batch - leaving batch in queue '{:}': {:}".format(work_queue, rex))
    return ret

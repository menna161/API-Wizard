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


def _upload_batch(self, queue):
    ret = {'count': 0}
    (batch_reversed, payload) = self.upload_cache.pop(queue, (None, None))
    if batch_reversed:
        log.info("Found cached batch with {:} entries for queue '{:}'".format(len(batch_reversed), queue))
        ret['continue'] = True
    else:
        batch_reversed = self.client.lrange(queue, (- self.options.get('max_batch_size', 100)), (- 1))
        if (not batch_reversed):
            if log.isEnabledFor(logging.DEBUG):
                log.debug("No batch found to upload from queue '{:}'".format(queue))
            return ret
        payload = self._prepare_payload_for(reversed(batch_reversed))
    try:
        (ok, msg) = self._upload(payload)
        if ok:
            log.info("Uploaded batch with {:} entries from queue '{:}'".format(len(batch_reversed), queue))
            ret['count'] = len(batch_reversed)
            self.client.pipeline().ltrim(queue, 0, (- (len(batch_reversed) + 1))).bgsave().execute()
        else:
            log.warning("Temporarily unable to upload batch with {:} entries from queue '{:}': {:}".format(len(batch_reversed), queue, msg))
            self.upload_cache[queue] = (batch_reversed, payload)
            ret['error'] = msg
    except RequestException as rex:
        if ((queue == self.PENDING_QUEUE) and (self.options.get('max_retry', 10) > 0)):
            retry_queue = self.RETRY_QUEUE.format(datetime.datetime.utcnow(), 0)
            log.warning("Failed to upload pending batch - transferring to new dedicated retry queue '{:}': {:}".format(retry_queue, rex))
            self.client.pipeline().lpush(retry_queue, *batch_reversed).ltrim(queue, 0, (- (len(batch_reversed) + 1))).bgsave().execute()
        else:
            log.warning("Failed to upload batch - leaving batch in queue '{:}': {:}".format(queue, rex))
        raise
    return ret

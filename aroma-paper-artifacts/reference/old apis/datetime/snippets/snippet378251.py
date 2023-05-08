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


def upload_retrying(self):
    ret = {'total': 0}
    queue_limit = self.options.get('retry_queue_limit', 10)
    queues = self.list_queues(pattern='retr_*')
    if queues:
        log.warning('Found {:}/{:} retry queue(s)'.format(len(queues), queue_limit))
    remaining_count = len(queues)
    for queue in queues:
        match = self.RETRY_QUEUE_REGEX.match(queue)
        if (not match):
            log.error("Failed to match retry queue name '{:}'".format(queue))
            continue
        attempt = (int(match.group('attempt')) + 1)
        entries = self.client.lrange(queue, 0, (- 1))
        payload = self._prepare_payload_for(entries)
        try:
            (ok, msg) = self._upload(payload, splay_factor=remaining_count)
            if ok:
                log.info("Sucessfully uploaded retry queue '{:}' with {:} entries".format(queue, len(entries)))
                self.client.pipeline().delete(queue).bgsave().execute()
                ret['total'] += len(entries)
                remaining_count -= 1
            else:
                log.warning('Temporarily unable to upload retry queue(s) - skipping remaining if present: {:}'.format(msg))
                ret.setdefault('errors', []).append(msg)
                break
        except RequestException as rex:
            ret.setdefault('errors', []).append(str(rex))
            max_retry = self.options.get('max_retry', 10)
            log.warning("Failed retry attempt {:}/{:} for uploading queue '{:}': {:}".format(attempt, max_retry, queue, rex))
            if (attempt >= max_retry):
                fail_queue = self.FAIL_QUEUE.format(datetime.datetime.utcnow())
                log.warning("Max retry attempt reached for queue '{:}' - transferring to fail queue '{:}'".format(queue, fail_queue))
                self.client.pipeline().lpush(fail_queue, *entries).expire(fail_queue, self.options.get('fail_ttl', 604800)).delete(queue).bgsave().execute()
            else:
                self.client.pipeline().renamenx(queue, re.sub('_#\\d+$', '_#{:}'.format(attempt), queue)).bgsave().execute()
    ret['is_overrun'] = (remaining_count >= queue_limit)
    return ret

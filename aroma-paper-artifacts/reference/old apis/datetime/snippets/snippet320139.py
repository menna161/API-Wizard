import itertools
import json
from datetime import datetime, timedelta
from time import sleep
from urllib.parse import urlparse
import salesforce_bulk


def bulk_api_query(self, sobject, query, date_time_fields, bulk_api_poll_interval):
    job = self._bulk.create_query_job(sobject, contentType='JSON')
    batch = self._bulk.query(job, query)
    self._bulk.close_job(job)
    while (not self._bulk.is_batch_done(batch)):
        sleep(bulk_api_poll_interval)
    for result in self._bulk.get_all_results_for_query_batch(batch):
        result = json.load(result)
        for rec in result:
            if (len(date_time_fields) > 0):
                for f in date_time_fields:
                    if (rec[f] is not None):
                        rec[f] = ((datetime.utcfromtimestamp(0) + timedelta(milliseconds=rec[f])).isoformat(timespec='milliseconds') + '+0000')
            (yield rec)

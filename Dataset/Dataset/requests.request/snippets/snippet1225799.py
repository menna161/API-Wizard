import requests
import logging
from crono import queue


@queue.queue.task(bind=True, name='crono.tasks.request')
def request(self, method, url, **kwargs):
    requests.request(method, url, **kwargs)

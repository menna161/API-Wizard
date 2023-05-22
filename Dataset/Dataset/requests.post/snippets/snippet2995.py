import logging
import requests
from nameko.dependency_providers import Config
from nameko.events import event_handler
from nameko.utils.retry import retry
from .logger import LoggingDependency
from .storages import RedisStorage


def _send(self, url, metadata):
    'POST metadata to url'
    try:
        response = requests.post(url, json={'data': metadata}, timeout=TIMEOUT)
    except (requests.Timeout, requests.RequestException) as e:
        raise WebhookUnreachableException('Unreachable', url, 503, original_exception=e)
    if ((response.status_code < 200) or (response.status_code >= 400)):
        raise WebhookUnreachableException('Unreachable', url, response.status_code)
    log('Successfully called webhook {url}'.format(url=url))

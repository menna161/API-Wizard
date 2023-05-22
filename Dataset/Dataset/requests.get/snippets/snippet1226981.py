import json
import logging
import socket
import time
from urllib.parse import urlparse
import datadog
import dns.rdatatype
import requests
from ddtrace import patch
from app.models.dinghy_data import DinghyData
from app.models.dinghy_dns import DinghyDNS
import requests


def process_request(protocol, domain, params, headers, redis_host):
    '\n    Internal method to run request process, takes protocol and domain for input\n    '
    if (protocol == ''):
        protocol = 'https'
    domain_response_code = ''
    domain_response_text = ''
    domain_response_time_ms = ''
    domain_response_headers = {}
    try:
        datadog.statsd.increment('dinghy_ping_http_connection_check.increment')
        r = requests.get(f'{protocol}://{domain}', params=params, timeout=5, headers=headers)
    except requests.exceptions.Timeout as err:
        domain_response_text = f'Timeout: {err}'
        datadog.statsd.increment('dinghy_ping_event_http_connection_check_fail_timeout.increment')
        return (domain_response_code, domain_response_text, domain_response_time_ms, domain_response_headers)
    except requests.exceptions.TooManyRedirects as err:
        domain_response_text = f'TooManyRedirects: {err}'
        datadog.statsd.increment('dinghy_ping_event_http_connection_check_fail_redirects.increment')
        return (domain_response_code, domain_response_text, domain_response_time_ms, domain_response_headers)
    except requests.exceptions.RequestException as err:
        domain_response_text = f'RequestException: {err}'
        datadog.statsd.increment('dinghy_ping_event_http_connection_check_fail_exception.increment')
        return (domain_response_code, domain_response_text, domain_response_time_ms, domain_response_headers)
    domain_response_code = r.status_code
    domain_response_text = r.text
    domain_response_headers = dict(r.headers)
    domain_response_time_ms = (r.elapsed.microseconds / 1000)
    d = DinghyData(redis_host, domain_response_code, domain_response_time_ms, r.url)
    d.save_ping()
    return (domain_response_code, domain_response_text, domain_response_time_ms, domain_response_headers)

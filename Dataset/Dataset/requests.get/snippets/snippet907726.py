import logging
import apache_beam as beam
import requests
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from requests.exceptions import RequestException
from google.api_core.exceptions import GoogleAPIError
from google.api_core.exceptions import ServerError
from google.auth.exceptions import GoogleAuthError
from google.cloud import storage


@beam.utils.retry.with_exponential_backoff(initial_delay_secs=10.0, num_retries=3, retry_filter=(lambda exception: isinstance(exception, ConnectionError)))
def wrapper_requests_call(self, asset_url, creative_id):
    request = requests.get(asset_url)
    status_code = request.status_code
    if (status_code == 200):
        content = request.content
        return content
    elif (status_code > 500):
        log_message = 'Requests server error-\n      status_code: {0}, creative_id: {1}'.format(status_code, creative_id)
        logging.warning(log_message)
        raise ConnectionError(log_message)
    else:
        log_message = 'Requests HTTP error-\n      status_code: {0}, creative_id: {1}'.format(status_code, creative_id)
        logging.warning(log_message)
        raise HTTPError(log_message)

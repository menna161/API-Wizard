from pandas import DataFrame
from pandas import json_normalize
import requests
import datetime
from urllib.parse import urljoin
from ratelimit import limits, RateLimitException
from backoff import on_exception, expo
from petpy.exceptions import PetfinderInvalidCredentials, PetfinderInsufficientAccess, PetfinderResourceNotFound, PetfinderUnexpectedError, PetfinderInvalidParameters, PetfinderRateLimitExceeded


def _get_result(self, url, headers, params=None):
    '\n\n        Parameters\n        ----------\n\n        Returns\n        -------\n\n        '
    r = requests.get(url, headers=headers, params=params)
    if (r.status_code == 400):
        raise PetfinderInvalidParameters(message='There are invalid parameters in the API query.', err=r.json()['invalid-params'])
    if (r.status_code == 401):
        if (r.json()['detail'] == 'Access token invalid or expired'):
            self._access_token = self._authenticate()
        else:
            raise PetfinderInvalidCredentials(message='Invalid Credentials', err=(r.reason, r.status_code))
    if (r.status_code == 403):
        raise PetfinderInsufficientAccess(message='Insufficient Access', err=(r.reason, r.status_code))
    if (r.status_code == 404):
        raise PetfinderResourceNotFound(message='Requested Resource not Found', err=(r.reason, r.status_code))
    if (r.status_code == 429):
        raise PetfinderRateLimitExceeded(message='Daily Rate Limit Exceed. Resets at 12:00am UTC', err=(r.reason, r.status_code))
    if (r.status_code == 500):
        raise PetfinderUnexpectedError(message='The Petfinder API encountered an unexpected error.', err=(r.reason, r.status_code))
    return r

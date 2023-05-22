from pandas import DataFrame
from pandas import json_normalize
import requests
import datetime
from urllib.parse import urljoin
from ratelimit import limits, RateLimitException
from backoff import on_exception, expo
from petpy.exceptions import PetfinderInvalidCredentials, PetfinderInsufficientAccess, PetfinderResourceNotFound, PetfinderUnexpectedError, PetfinderInvalidParameters, PetfinderRateLimitExceeded


def _authenticate(self):
    '\n        Internal function for authenticating users to the Petfinder API.\n\n        Raises\n        ------\n        PetfinderInvalidCredentials\n            Raised if the supplied secret key and secret access key are invalid. Check the generated API key from\n            petfinder.com is still active and that the secret and access keys are the same as those passed.\n\n        Returns\n        -------\n        str\n            Access token granted by the Petfinder API. The access token stays live for 3600 seconds, or one hour,\n            at which point the user must reauthenticate.\n\n        See Also\n        --------\n        PetfinderInvalidCredentials\n\n        '
    endpoint = 'oauth2/token'
    url = urljoin(self._host, endpoint)
    data = {'grant_type': 'client_credentials', 'client_id': self.key, 'client_secret': self.secret}
    r = requests.post(url, data=data)
    if (r.status_code == 401):
        raise PetfinderInvalidCredentials(message=r.reason, err='Invalid Credentials')
    return r.json()['access_token']

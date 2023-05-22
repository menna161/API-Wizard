import requests
from unsplash.errors import UnsplashError


def _request(self, url, method, params=None, data=None, **kwargs):
    url = ('%s%s' % (self.api.base_url, url))
    headers = self.get_auth_header()
    headers.update(self.get_version_header())
    headers.update(kwargs.pop('headers', {}))
    try:
        response = requests.request(method, url, params=params, data=data, headers=headers, **kwargs)
    except Exception as e:
        raise UnsplashError(('Connection error: %s' % e))
    try:
        if (not self._is_2xx(response.status_code)):
            if (response.text == self.rate_limit_error):
                raise UnsplashError(self.rate_limit_error)
            else:
                errors = response.json().get('errors')
                raise UnsplashError((errors[0] if errors else None))
        result = response.json()
    except ValueError as e:
        result = None
    return result

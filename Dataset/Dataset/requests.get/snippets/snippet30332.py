from dexy.exceptions import UserFeedback
from dexy.filter import DexyFilter
import json
import mimetypes
import os
import requests


def get_path(self, path, params=None):
    response = requests.get(self.url_for_path(path), params=params, **self.credentials())
    self.handle_response_code(response)
    return response.json()

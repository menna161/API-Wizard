from dexy.exceptions import UserFeedback
from dexy.filter import DexyFilter
import json
import mimetypes
import os
import requests


def json_put_path(self, path, data=None):
    response = requests.put(self.url_for_path(path), data=json.dumps(data), **self.credentials_with_json_content_type())
    self.handle_response_code(response)
    return response.json()

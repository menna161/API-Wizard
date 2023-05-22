from dexy.exceptions import UserFeedback
from dexy.filter import DexyFilter
import json
import mimetypes
import os
import requests


def delete_path(self, path):
    response = requests.delete(self.url_for_path(path), **self.credentials())
    self.handle_response_code(response)
    return response.json()

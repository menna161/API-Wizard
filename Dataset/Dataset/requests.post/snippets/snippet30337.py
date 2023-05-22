from dexy.exceptions import UserFeedback
from dexy.filter import DexyFilter
import json
import mimetypes
import os
import requests


def post_file(self, path, canonical_name, filepath):
    no_check = {'X-Atlassian-Token': 'no-check'}
    mimetype = self.guess_mimetype(canonical_name)
    with open(filepath, 'rb') as fileref:
        files = {'file': (canonical_name, fileref, mimetype), 'comment': str(self.setting('attachment-comment')), 'minorEdit': self.attachment_minor_edit_setting()}
        response = requests.post(self.url_for_path(path), files=files, **self.credentials_with_headers(no_check))
    self.handle_response_code(response)
    return response.json()

from __future__ import unicode_literals
import json
import os
import shutil
import time
from random import randint
from requests_toolbelt import MultipartEncoder
from . import config
from .api_photo import get_image_size, stories_shaper


def configure_story(self, upload_id, photo):
    (w, h) = get_image_size(photo)
    data = self.json_data({'source_type': 4, 'upload_id': upload_id, 'story_media_creation_date': str((int(time.time()) - randint(11, 20))), 'client_shared_at': str((int(time.time()) - randint(3, 10))), 'client_timestamp': str(int(time.time())), 'configure_mode': 1, 'device': self.device_settings, 'edits': {'crop_original_size': [(w * 1.0), (h * 1.0)], 'crop_center': [0.0, 0.0], 'crop_zoom': 1.3333334}, 'extra': {'source_width': w, 'source_height': h}})
    return self.send_request('media/configure_to_story/?', data)

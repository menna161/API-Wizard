from __future__ import unicode_literals
import json
import os
import re
import shutil
import subprocess
import time
import random
from uuid import uuid4
from . import config
from math import ceil
import moviepy.editor as mp


def upload_video(self, video, caption=None, upload_id=None, thumbnail=None, options={}):
    'Upload video to Instagram\n\n    @param video      Path to video file (String)\n    @param caption    Media description (String)\n    @param upload_id  Unique upload_id (String). When None, then generate\n                      automatically\n    @param thumbnail  Path to thumbnail for video (String). When None, then\n                      thumbnail is generate automatically\n    @param options    Object with difference options, e.g. configure_timeout,\n                      rename_thumbnail, rename (Dict)\n                      Designed to reduce the number of function arguments!\n                      This is the simplest request object.\n\n    @return           Object with state of uploading to Instagram (or False)\n    '
    options = dict({'configure_timeout': 15, 'rename_thumbnail': True, 'rename': True}, **(options or {}))
    if (upload_id is None):
        upload_id = str(int((time.time() * 1000)))
    (video, thumbnail, width, height, duration) = resize_video(video, thumbnail)
    waterfall_id = str(uuid4())
    upload_name = '{upload_id}_0_{rand}'.format(upload_id=upload_id, rand=random.randint(1000000000, 9999999999))
    rupload_params = {'retry_context': '{"num_step_auto_retry":0,"num_reupload":0,"num_step_manual_retry":0}', 'media_type': '2', 'xsharing_user_ids': '[]', 'upload_id': upload_id, 'upload_media_duration_ms': str(int((duration * 1000))), 'upload_media_width': str(width), 'upload_media_height': str(height)}
    self.session.headers.update({'Accept-Encoding': 'gzip', 'X-Instagram-Rupload-Params': json.dumps(rupload_params), 'X_FB_VIDEO_WATERFALL_ID': waterfall_id, 'X-Entity-Type': 'video/mp4'})
    response = self.session.get('https://{domain}/rupload_igvideo/{name}'.format(domain=config.API_DOMAIN, name=upload_name))
    if (response.status_code != 200):
        return False
    video_data = open(video, 'rb').read()
    video_len = str(len(video_data))
    self.session.headers.update({'Offset': '0', 'X-Entity-Name': upload_name, 'X-Entity-Length': video_len, 'Content-Type': 'application/octet-stream', 'Content-Length': video_len})
    response = self.session.post('https://{domain}/rupload_igvideo/{name}'.format(domain=config.API_DOMAIN, name=upload_name), data=video_data)
    if (response.status_code != 200):
        return False
    configure_timeout = options.get('configure_timeout')
    for attempt in range(4):
        if configure_timeout:
            time.sleep(configure_timeout)
        if self.configure_video(upload_id, video, thumbnail, width, height, duration, caption, options=options):
            media = self.last_json.get('media')
            self.expose()
            if options.get('rename'):
                os.rename(video, '{fname}.REMOVE_ME'.format(fname=video))
            return media
    return False

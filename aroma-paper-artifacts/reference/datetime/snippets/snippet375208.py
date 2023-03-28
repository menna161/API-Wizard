import datetime, hashlib, hmac
import cv2
import requests
import math
import getpass
import boto3
from botocore.exceptions import ClientError
from video_capture import VideoCapture
from detector import Detector
from viewer import Viewer


def _update_name_list(self):
    limit_time = (datetime.datetime.now() - datetime.timedelta(seconds=self.NAME_TTL_SEC))
    for d in self.recent_name_list[:]:
        if (d.get('timestamp') < limit_time):
            self.recent_name_list.remove(d)

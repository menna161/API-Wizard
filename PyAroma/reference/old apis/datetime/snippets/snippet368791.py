import json
import locale
import logging
from datetime import datetime
import requests
from PIL import Image, ImageFont


def nowISO(self):
    'Return the current utc time in ISO8601 timestamp format.'
    return datetime.utcnow().isoformat()

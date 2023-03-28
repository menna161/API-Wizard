import re
import json
import random
import requests
from pprint import pprint


def get_certificates(self):
    "Get user's certificates."
    for certificate in self.user_data.certificates:
        certificate['datetime'] = certificate['datetime'].strip()
    return self.user_data.certificates

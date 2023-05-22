import json
import requests
import sys, cgi, os, gzip
from StringIO import BytesIO
from io import BytesIO


def _get(self, url):
    bearer_headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Bearer {0}'.format(self.token)}
    response = requests.get(url, params=None, headers=bearer_headers, stream=True)
    return response

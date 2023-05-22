import requests
import tarfile
import tempfile
import json
import os
from os import listdir
from os.path import isfile, join, isdir
import uuid
import hashlib
import json
import gzip
import shutil
from requests.auth import HTTPBasicAuth
from . import ManifestCreator


def pushManifest(self, manifest, image, tag):
    headers = {'Content-Type': 'application/vnd.docker.distribution.manifest.v2+json'}
    url = ((((self.registryPath + '/v2/') + image) + '/manifests/') + tag)
    r = requests.put(url, headers=headers, data=manifest, auth=self.auth, verify=self.sslVerify)
    return (r.status_code == 201)

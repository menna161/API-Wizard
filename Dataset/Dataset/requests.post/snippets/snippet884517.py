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


def startPushing(self, repository):
    self.conditionalPrint('[INFO] Upload started')
    r = requests.post((((self.registryPath + '/v2/') + repository) + '/blobs/uploads/'), auth=self.auth, verify=self.sslVerify)
    uploadUrl = None
    if r.headers.get('Location', None):
        uploadUrl = r.headers.get('Location')
    return ((r.status_code == 202), uploadUrl)

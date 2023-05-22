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


def chunkedUpload(self, file, url):
    content_name = str(file)
    content_path = os.path.abspath(file)
    content_size = os.stat(content_path).st_size
    f = open(content_path, 'rb')
    index = 0
    offset = 0
    headers = {}
    indexneu = 0
    uploadUrl = url
    sha256hash = hashlib.sha256()
    for chunk in self.read_in_chunks(f, sha256hash):
        if ('http' not in uploadUrl):
            uploadUrl = (self.registryPath + uploadUrl)
        offset = (index + len(chunk))
        headers['Content-Type'] = 'application/octet-stream'
        headers['Content-Length'] = str(len(chunk))
        headers['Content-Range'] = ('%s-%s' % (index, offset))
        index = offset
        last = False
        if (offset == content_size):
            last = True
        try:
            self.conditionalPrint((('Pushing... ' + str(round(((offset / content_size) * 100), 2))) + '%  '), end='\r')
            if last:
                r = requests.put(((uploadUrl + '&digest=sha256:') + str(sha256hash.hexdigest())), data=chunk, headers=headers, auth=self.auth, verify=self.sslVerify)
            else:
                r = requests.patch(uploadUrl, data=chunk, headers=headers, auth=self.auth, verify=self.sslVerify)
                if ('Location' in r.headers):
                    uploadUrl = r.headers['Location']
        except Exception as e:
            self.conditionalPrint(('[ERROR] ' + str(e)))
            return False
    f.close()
    self.conditionalPrint('')

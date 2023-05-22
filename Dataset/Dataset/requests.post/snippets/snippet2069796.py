import requests
import time
import json
import re
import logging, os, sys
from ..utils import SSH


def __init__(self, cloud):
    self.log = logging.getLogger(os.path.basename(__file__).split('.')[0].upper())
    if (not len(self.log.handlers)):
        self.log.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)
    self._cloud = cloud
    self._credential = cloud.platform_credential
    self._headers = {'Content-Type': 'application/json'}
    self.endpoint = self._credential['endpoint']
    token = requests.post(url=(self.endpoint + '/v3/auth/tokens'), headers=self._headers, data=json.dumps({'auth': {'identity': {'methods': ['password'], 'password': {'user': {'domain': {'id': 'default'}, 'name': self._credential['username'], 'password': self._credential['password']}}}, 'scope': {'project': {'domain': {'id': 'default'}, 'name': self._credential['project_name']}}}})).headers['X-Subject-Token']
    self._token = token
    self._headers['X-Auth-Token'] = token
    self.project_id = requests.get(url=((self.endpoint + '/v3/projects?name=') + self._credential['project_name']), headers=self._headers).json()['projects'][0]['id']
    self.tenant_endpoint = ('/v2/' + self.project_id)
    self.instances = InstanceManager(self)
    self.volumes = VolumeManager(self)
    self.images = ImageManager(self)
    self.flavors = FlavorManager(self)
    self.keypairs = KeyManager()

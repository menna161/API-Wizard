import unittest
import requests
import docker
from dockertarpusher import Registry


def testOneLayer(self):
    registryUrl = 'http://localhost:5000'
    reg = Registry(registryUrl, 'tests/busybox.tar')
    reg.processImage()
    r = requests.get((registryUrl + '/v2/_catalog'))
    self.assertTrue(('razikus/busybox' in r.json()['repositories']))
    r = requests.get((registryUrl + '/v2/razikus/busybox/tags/list'))
    self.assertTrue(('razikus/busybox' == r.json()['name']))
    self.assertTrue(('1.31' in r.json()['tags']))

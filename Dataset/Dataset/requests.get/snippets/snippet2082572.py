import http.client
import json
import urllib
from http.client import ssl
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import requests
from devicedata.providers.base_provider import BaseDeviceInfo
from devicedata.providers.base_provider import BaseProvider
from devicedata.providers.base_provider import DeviceInfoEntry
from devicedata.providers.base_provider import FormattedDeviceInfoEntry
from devicedata.providers.base_provider import SoftwareEntry
from devicedata.providers.base_provider import build_full_hostname
from devicedata.providers.helpers import format_bytes


@staticmethod
def __run_query(query):
    if (not hasattr(settings, 'PUPPETDB_SETTINGS')):
        return
    params = urllib.parse.urlencode({'query': query})
    if (settings.PUPPETDB_SETTINGS['ignore_ssl'] is not True):
        context = ssl.create_default_context(cafile=settings.PUPPETDB_SETTINGS['cacert'])
        context.load_cert_chain(certfile=settings.PUPPETDB_SETTINGS['cert'], keyfile=settings.PUPPETDB_SETTINGS['key'])
        conn = http.client.HTTPSConnection(settings.PUPPETDB_SETTINGS['host'], settings.PUPPETDB_SETTINGS['port'], context=context)
        conn.request('GET', (settings.PUPPETDB_SETTINGS['req'] + params))
        res = conn.getresponse()
        if ((res is None) or (res.status != http.client.OK)):
            raise ValidationError('Puppet')
        try:
            body = json.loads(res.read().decode())
        except:
            raise ValidationError('Puppet')
    else:
        host = ((settings.PUPPETDB_SETTINGS['host'] + ':') + str(settings.PUPPETDB_SETTINGS['port']))
        if ('http' not in host):
            host = ('http://' + host)
        res = requests.get(((host + settings.PUPPETDB_SETTINGS['req']) + params), verify=False)
        body = res.json()
    if (len(body) == 0):
        raise ObjectDoesNotExist()
    return body

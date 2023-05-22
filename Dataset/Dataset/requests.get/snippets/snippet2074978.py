from json.decoder import JSONDecodeError
import time
import requests
from requests.exceptions import RequestException
from .owlet import Owlet
from .owletexceptions import OwletTemporaryCommunicationException
from .owletexceptions import OwletPermanentCommunicationException
from .owletexceptions import OwletNotInitializedException


def update_devices(self):
    'Update list of devices from the cloud.'
    token = self.get_auth_token()
    if (token is None):
        raise OwletNotInitializedException('Please login first')
    devices_url = (self.base_properties_url + 'devices.json')
    devices_headers = self.get_request_headers()
    try:
        result = requests.get(devices_url, headers=devices_headers, timeout=5)
    except RequestException:
        raise OwletTemporaryCommunicationException('Server request failed - no response')
    if (result.status_code != 200):
        raise OwletTemporaryCommunicationException('Server request failed - status code')
    try:
        json_result = result.json()
    except JSONDecodeError:
        raise OwletTemporaryCommunicationException('Server did not send valid json')
    self._devices = []
    for device in json_result:
        new_device = Owlet(self, device['device'])
        self._devices.append(new_device)
    return self._devices

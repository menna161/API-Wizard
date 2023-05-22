from json.decoder import JSONDecodeError
import requests
from requests.exceptions import RequestException
from .owletproperty import OwletProperty
from .owletexceptions import OwletTemporaryCommunicationException
from .owletexceptions import OwletNotInitializedException


def reactivate(self):
    '(Re-)Activate streaming of Owlet attributes.'
    if (not self.properties):
        raise OwletNotInitializedException('Initialize first - no properties')
    if ('APP_ACTIVE' not in self.properties):
        raise OwletNotInitializedException('Initialize first - missing property')
    key = self.properties['APP_ACTIVE'].key
    reactivate_url = (self.owlet_api.base_properties_url + 'properties/{}/datapoints'.format(key))
    reactivate_headers = self.owlet_api.get_request_headers()
    reactivate_payload = {'datapoints': {'value': 1}}
    try:
        result = requests.post(reactivate_url, json=reactivate_payload, headers=reactivate_headers, timeout=5)
    except RequestException:
        raise OwletTemporaryCommunicationException('Server Request failed - no response')
    if (result.status_code != 201):
        raise OwletTemporaryCommunicationException(('Server Request failed, return code %s' % result.status_code))

from json.decoder import JSONDecodeError
import requests
from requests.exceptions import RequestException
from .owletproperty import OwletProperty
from .owletexceptions import OwletTemporaryCommunicationException
from .owletexceptions import OwletNotInitializedException


def update(self):
    'Update attributes of the Owlet.'
    properties_url = (self.owlet_api.base_properties_url + 'dsns/{}/properties'.format(self.dsn))
    properties_header = self.owlet_api.get_request_headers()
    try:
        result = requests.get(properties_url, headers=properties_header)
    except RequestException:
        raise OwletTemporaryCommunicationException('Server Request failed - no response')
    if (result.status_code != 200):
        raise OwletTemporaryCommunicationException('Server Request failed - status code')
    try:
        json = result.json()
    except JSONDecodeError:
        raise OwletTemporaryCommunicationException('Update failed - JSON error')
    for myproperty in json:
        property_name = myproperty['property']['name']
        if (property_name in self.properties):
            self.properties[property_name].update(myproperty['property'])
        else:
            new_property = OwletProperty(myproperty['property'])
            self.properties[new_property.name] = new_property
    for (name, myproperty) in self.properties.items():
        if (name == 'APP_ACTIVE'):
            continue
        if ((self.update_interval is None) or ((myproperty.minimum_update_interval is not None) and (myproperty.minimum_update_interval > 0) and (myproperty.minimum_update_interval < self.update_interval))):
            self.update_interval = myproperty.minimum_update_interval

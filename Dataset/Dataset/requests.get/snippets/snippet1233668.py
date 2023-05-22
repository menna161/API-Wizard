import requests
from oslo_log import log as logging
from tempest.lib import decorators
from designate_tempest_plugin.tests import base
from designate_tempest_plugin.services.dns.v2.json import base as service_base
from tempest import config


@decorators.idempotent_id('aa84986e-f2ad-11eb-b58d-74e5f9e2a801')
def test_list_enabled_api_versions(self):
    for user in ['admin', 'primary', 'not_auth_user']:
        if (user == 'admin'):
            ver_doc = self.admin_client.list_enabled_api_versions()[1]
            try:
                versions = ver_doc['versions']['values']
            except TypeError:
                versions = ver_doc['versions']
        if (user == 'primary'):
            ver_doc = self.primary_client.list_enabled_api_versions()[1]
            try:
                versions = ver_doc['versions']['values']
            except TypeError:
                versions = ver_doc['versions']
        if (user == 'not_auth_user'):
            response = requests.get(self.primary_client.base_url, verify=False)
            headers = {k.lower(): v.lower() for (k, v) in response.headers.items()}
            try:
                versions = self.deserialize(headers, str(response.text))['versions']['values']
            except TypeError:
                versions = self.deserialize(headers, str(response.text))['versions']
        LOG.info('Received enabled API versions for {} user are:{}'.format(user, versions))
        enabled_ids = {item['id'] for item in versions}
        LOG.info('Enabled versions IDs are:{}'.format(enabled_ids))
        base_versions = {'v1', 'v2', 'v2.0'}
        self.assertFalse(enabled_ids.isdisjoint(base_versions), 'Failed, at least one base API version: {} was not found in the API version list: {}'.format(base_versions, enabled_ids))

import random
from oslo_log import log as logging
from oslo_utils import versionutils
from tempest import config
from tempest.lib import decorators
from tempest.lib import exceptions as lib_exc
from tempest.lib.common.utils import data_utils
import tempest.test
from designate_tempest_plugin.tests import base
from designate_tempest_plugin import data_utils as dns_data_utils
from designate_tempest_plugin.common import constants as const
from designate_tempest_plugin.common import exceptions


def _reach_quota_limit(self, limit_threshold, quota_type, zone=None):
    attempt_number = 0
    not_raised_msg = "Failed, expected '413 over_quota' response of type:{} wasn't received.".format(quota_type)
    while (attempt_number <= (limit_threshold + 1)):
        try:
            attempt_number += 1
            LOG.info('Attempt No:{} '.format(attempt_number))
            if (quota_type == 'zones_quota'):
                zone_name = dns_data_utils.rand_zone_name(name='_reach_quota_limit', suffix=self.tld_name)
                zone = self.zones_client.create_zone(name=zone_name, description='Test zone for:{}'.format(quota_type))[1]
                self.addCleanup(self.wait_zone_delete, self.zones_client, zone['id'])
            else:
                if (quota_type == 'zone_recordsets'):
                    max_number_of_records = 10
                    prj_quota = self.admin_client.show_quotas(project_id=self.zones_client.project_id, headers=self.all_projects_header)[1]['zone_records']
                    if (max_number_of_records > prj_quota):
                        max_number_of_records = prj_quota
                    recordset_data = dns_data_utils.rand_recordset_data(record_type='A', zone_name=zone['name'], number_of_records=random.randint(1, max_number_of_records))
                else:
                    recordset_data = dns_data_utils.rand_recordset_data(record_type='A', zone_name=zone['name'])
                recordset = self.recordset_client.create_recordset(zone['id'], recordset_data=recordset_data, wait_until=const.ACTIVE)[1]
                self.addCleanup(self.wait_recordset_delete, self.recordset_client, zone['id'], recordset['id'])
            self.assertLess(attempt_number, (limit_threshold + 1), not_raised_msg)
        except Exception as e:
            raised_err = str(e).replace(' ', '')
            if (not_raised_msg in str(e)):
                raise AssertionError(not_raised_msg)
            elif (("'code':413" in raised_err) and ("'type':'over_quota'" in raised_err)):
                LOG.info("OK, type':'over_quota' was raised")
                break
            else:
                raise

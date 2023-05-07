from unittest import TestCase
from cloudshell.api.cloudshell_api import ResourceInfoVmDetails, ResourceInfo, VmCustomParam
from cloudshell.cp.vcenter.models import GenericDeployedAppResourceModel
from mock import Mock, create_autospec
from cloudshell.cp.vcenter.commands.refresh_ip import RefreshIpCommand
from cloudshell.cp.vcenter.models.VMwarevCenterResourceModel import VMwarevCenterResourceModel
from cloudshell.cp.vcenter.common.model_factory import ResourceModelParser


def test_refresh_ip_choose_ipv4(self):
    nic1 = Mock()
    nic1.network = 'A Network'
    nic1.ipAddress = ['192.168.1.1']
    nic2 = Mock()
    nic2.network = 'A Network'
    nic2.ipAddress = ['2001:0db8:0a0b:12f0:0000:0000:0000:0001']
    guest = Mock()
    guest.toolsStatus = 'toolsOk'
    guest.net = [nic1, nic2]
    vm = Mock()
    vm.guest = guest
    pyvmomi_service = Mock()
    pyvmomi_service.find_by_uuid = Mock(return_value=vm)
    ip_regex = self._create_custom_param('ip_regex', '')
    refresh_ip_timeout = self._create_custom_param('refresh_ip_timeout', '10')
    resource_model = create_autospec(GenericDeployedAppResourceModel)
    resource_model.fullname = 'Generic Deployed App'
    resource_model.vm_uuid = ('123',)
    resource_model.cloud_provider = 'vCenter'
    resource_model.vm_custom_params = [ip_regex, refresh_ip_timeout]
    refresh_ip_command = RefreshIpCommand(pyvmomi_service, ResourceModelParser(), Mock())
    session = Mock()
    session.UpdateResourceAddress = Mock(return_value=True)
    session.GetResourceDetails = Mock(return_value=resource_model)
    si = Mock()
    center_resource_model = VMwarevCenterResourceModel()
    center_resource_model.default_datacenter = 'QualiSB'
    center_resource_model.holding_network = 'anetwork'
    cancellation_context = Mock()
    refresh_ip_command.refresh_ip(si=si, session=session, vcenter_data_model=center_resource_model, resource_model=resource_model, cancellation_context=cancellation_context, logger=Mock(), app_request_json=Mock())
    self.assertTrue(session.UpdateResourceAddress.called_with('machine1', '192.168.1.1'))

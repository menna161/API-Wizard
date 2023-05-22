from unittest import TestCase
from mock import Mock
from pyVmomi import vim
from cloudshell.cp.vcenter.commands.disconnect_dvswitch import VirtualSwitchToMachineDisconnectCommand
from cloudshell.cp.vcenter.models.VMwarevCenterResourceModel import VMwarevCenterResourceModel
from cloudshell.cp.vcenter.network.vnic.vnic_service import VNicService


def test_delete_all(self):
    uuid = 'uuid'
    si = Mock()
    vm = Mock()
    connection_detail = Mock()
    connection_detail.host = Mock()
    connection_detail.username = Mock()
    connection_detail.password = Mock()
    connection_detail.port = Mock()
    pv_service = Mock()
    pv_service.connect = Mock(return_value=si)
    pv_service.find_by_uuid = Mock(return_value=vm)
    connector = VirtualSwitchToMachineDisconnectCommand(pv_service, Mock(), 'anetwork')
    connector.get_network_by_name = (lambda x, y: Mock())
    vcenter_data_model = VMwarevCenterResourceModel()
    res = connector.disconnect(si=si, logger=Mock(), vcenter_data_model=vcenter_data_model, vm_uuid=uuid, network_name=None, vm=None)
    self.assertTrue(pv_service.connect.called_with(connection_detail.host, connection_detail.username, connection_detail.password, connection_detail.port))
    self.assertTrue(pv_service.find_by_uuid.called_with(si, uuid))
    self.assertTrue(res)

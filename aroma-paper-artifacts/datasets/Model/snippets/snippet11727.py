from unittest import TestCase
from cloudshell.cp.vcenter.models.VMwarevCenterResourceModel import VMwarevCenterResourceModel
from mock import Mock
from cloudshell.cp.vcenter.models.DeployDataHolder import DeployDataHolder
from cloudshell.cp.vcenter.models.DeployFromTemplateDetails import DeployFromTemplateDetails
from cloudshell.cp.vcenter.models.VCenterDeployVMFromLinkedCloneResourceModel import VCenterDeployVMFromLinkedCloneResourceModel
from cloudshell.cp.vcenter.models.vCenterCloneVMFromVMResourceModel import vCenterCloneVMFromVMResourceModel
from cloudshell.cp.vcenter.models.vCenterVMFromTemplateResourceModel import vCenterVMFromTemplateResourceModel
from cloudshell.cp.vcenter.vm.deploy import VirtualMachineDeployer
from cloudshell.cp.vcenter.common.model_factory import ResourceModelParser


def _create_vcenter_resource_context(self):
    vc = VMwarevCenterResourceModel()
    vc.user = 'user'
    vc.password = '123'
    vc.default_dvswitch = 'switch1'
    vc.holding_network = 'anetwork'
    vc.vm_cluster = 'Quali'
    vc.vm_location = 'Quali'
    vc.vm_resource_pool = 'Quali'
    vc.vm_storage = 'Quali'
    vc.shutdown_method = 'hard'
    vc.ovf_tool_path = 'C\\program files\\ovf'
    vc.execution_server_selector = ''
    vc.reserved_networks = 'vlan65'
    vc.default_datacenter = 'QualiSB'
    return vc

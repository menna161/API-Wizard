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


def test_clone_deployer(self):
    deploy_from_template_details = DeployFromTemplateDetails(vCenterCloneVMFromVMResourceModel(), 'VM Deployment')
    deploy_from_template_details.template_resource_model.vcenter_name = 'vcenter_resource_name'
    deploy_from_template_details.vcenter_vm = 'name'
    resource_context = self._create_vcenter_resource_context()
    reservation_id = Mock()
    cancellation_context = Mock()
    cancellation_context.is_cancelled = False
    res = self.deployer.deploy_clone_from_vm(si=self.si, data_holder=deploy_from_template_details, vcenter_data_model=resource_context, logger=Mock(), reservation_id=reservation_id, cancellation_context=cancellation_context)
    self.assertEqual(res.vmName, self.name)
    self.assertEqual(res.vmUuid, self.uuid)
    self.pv_service.CloneVmParameters.assert_called()

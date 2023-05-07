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


def test_vm_deployer_error(self):
    self.clone_res.error = Mock()
    self.pv_service.CloneVmParameters = Mock(return_value=self.clone_parmas)
    self.pv_service.clone_vm = Mock(return_value=self.clone_res)
    deploy_from_template_details = DeployFromTemplateDetails(vCenterVMFromTemplateResourceModel(), 'VM Deployment')
    deploy_from_template_details.template_resource_model.vcenter_name = 'vcenter_resource_name'
    vcenter_data_model = self._create_vcenter_resource_context()
    self.assertRaises(Exception, self.deployer.deploy_from_template, self.si, Mock(), deploy_from_template_details, vcenter_data_model, Mock(), Mock())
    self.pv_service.CloneVmParameters.assert_called()

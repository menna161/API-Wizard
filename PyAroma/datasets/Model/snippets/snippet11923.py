import traceback
from cloudshell.cp.core.models import DeployAppResult
from cloudshell.cp.core.utils import convert_to_bool
from cloudshell.cp.vcenter.models.VCenterDeployVMFromLinkedCloneResourceModel import VCenterDeployVMFromLinkedCloneResourceModel
from cloudshell.cp.vcenter.models.vCenterCloneVMFromVMResourceModel import vCenterCloneVMFromVMResourceModel
from cloudshell.cp.vcenter.models.vCenterVMFromImageResourceModel import vCenterVMFromImageResourceModel
from cloudshell.cp.vcenter.models.vCenterVMFromTemplateResourceModel import vCenterVMFromTemplateResourceModel
from cloudshell.cp.vcenter.vm.ovf_image_params import OvfImageParams
from cloudshell.cp.vcenter.vm.vcenter_details_factory import VCenterDetailsFactory
from cloudshell.cp.vcenter.common.vcenter.vm_location import VMLocation
from cloudshell.cp.vcenter.common.cloud_shell.conn_details_retriever import ResourceConnectionDetailsRetriever
from cloudshell.cp.core.models import VmDetailsProperty


def _safely_get_vm_details(self, vm, vm_name, vcenter_model, deploy_model, logger):
    data = None
    try:
        data = self.vm_details_provider.create(vm=vm, name=vm_name, reserved_networks=vcenter_model.reserved_networks, ip_regex=deploy_model.ip_regex, deployment_details_provider=DeploymentDetailsProviderFromTemplateModel(deploy_model), wait_for_ip=deploy_model.wait_for_ip, logger=logger)
    except Exception:
        logger.error("Error getting vm details for '{0}': {1}".format(vm_name, traceback.format_exc()))
    return data

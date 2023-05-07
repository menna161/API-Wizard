import time
from datetime import datetime
import jsonpickle
from cloudshell.cp.vcenter.commands.vm_details import VmDetailsCommand
from cloudshell.cp.vcenter.models.DeployFromImageDetails import DeployFromImageDetails
from cloudshell.shell.core.context import ResourceRemoteCommandContext
from cloudshell.shell.core.driver_context import CancellationContext
from cloudshell.cp.vcenter.models.OrchestrationSaveResult import OrchestrationSaveResult
from cloudshell.cp.vcenter.models.OrchestrationSavedArtifactsInfo import OrchestrationSavedArtifactsInfo
from cloudshell.cp.vcenter.models.OrchestrationSavedArtifact import OrchestrationSavedArtifact
from pyVim.connect import SmartConnect, Disconnect
from cloudshell.cp.vcenter.commands.connect_dvswitch import VirtualSwitchConnectCommand
from cloudshell.cp.vcenter.commands.connect_orchestrator import ConnectionCommandOrchestrator
from cloudshell.cp.vcenter.commands.deploy_vm import DeployCommand
from cloudshell.cp.vcenter.commands.DeleteInstance import DestroyVirtualMachineCommand
from cloudshell.cp.vcenter.commands.disconnect_dvswitch import VirtualSwitchToMachineDisconnectCommand
from cloudshell.cp.vcenter.commands.load_vm import VMLoader
from cloudshell.cp.vcenter.commands.power_manager_vm import VirtualMachinePowerManagementCommand
from cloudshell.cp.vcenter.commands.refresh_ip import RefreshIpCommand
from cloudshell.cp.vcenter.commands.restore_snapshot import SnapshotRestoreCommand
from cloudshell.cp.vcenter.commands.save_snapshot import SaveSnapshotCommand
from cloudshell.cp.vcenter.commands.retrieve_snapshots import RetrieveSnapshotsCommand
from cloudshell.cp.vcenter.commands.save_sandbox import SaveAppCommand
from cloudshell.cp.vcenter.commands.delete_saved_sandbox import DeleteSavedSandboxCommand
from cloudshell.cp.vcenter.common.cloud_shell.resource_remover import CloudshellResourceRemover
from cloudshell.cp.vcenter.common.model_factory import ResourceModelParser
from cloudshell.cp.vcenter.common.utilites.command_result import set_command_result, get_result_from_command_output
from cloudshell.cp.vcenter.common.utilites.common_name import generate_unique_name
from cloudshell.cp.vcenter.common.utilites.context_based_logger_factory import ContextBasedLoggerFactory
from cloudshell.cp.vcenter.common.vcenter.ovf_service import OvfImageDeployerService
from cloudshell.cp.vcenter.common.vcenter.task_waiter import SynchronousTaskWaiter
from cloudshell.cp.vcenter.common.vcenter.vmomi_service import pyVmomiService
from cloudshell.cp.vcenter.common.wrappers.command_wrapper import CommandWrapper
from cloudshell.cp.vcenter.models.DeployDataHolder import DeployDataHolder
from cloudshell.cp.vcenter.models.DriverResponse import DriverResponse, DriverResponseRoot
from cloudshell.cp.vcenter.models.GenericDeployedAppResourceModel import GenericDeployedAppResourceModel
from cloudshell.cp.vcenter.models.VCenterDeployVMFromLinkedCloneResourceModel import VCenterDeployVMFromLinkedCloneResourceModel
from cloudshell.cp.vcenter.models.vCenterCloneVMFromVMResourceModel import vCenterCloneVMFromVMResourceModel
from cloudshell.cp.vcenter.models.vCenterVMFromImageResourceModel import vCenterVMFromImageResourceModel
from cloudshell.cp.vcenter.models.vCenterVMFromTemplateResourceModel import vCenterVMFromTemplateResourceModel
from cloudshell.cp.vcenter.network.dvswitch.creator import DvPortGroupCreator
from cloudshell.cp.vcenter.network.dvswitch.name_generator import DvPortGroupNameGenerator
from cloudshell.cp.vcenter.network.vlan.factory import VlanSpecFactory
from cloudshell.cp.vcenter.network.vlan.range_parser import VLanIdRangeParser
from cloudshell.cp.vcenter.network.vnic.vnic_service import VNicService
from cloudshell.cp.vcenter.vm.deploy import VirtualMachineDeployer
from cloudshell.cp.vcenter.vm.dvswitch_connector import VirtualSwitchToMachineConnector
from cloudshell.cp.vcenter.vm.ip_manager import VMIPManager
from cloudshell.cp.vcenter.vm.portgroup_configurer import VirtualMachinePortGroupConfigurer
from cloudshell.cp.vcenter.vm.vm_details_provider import VmDetailsProvider
from cloudshell.cp.vcenter.vm.vnic_to_network_mapper import VnicToNetworkMapper
from cloudshell.cp.vcenter.models.DeployFromTemplateDetails import DeployFromTemplateDetails
from cloudshell.cp.core.models import DeployApp, DeployAppResult, SaveApp, SaveAppResult
from cloudshell.cp.vcenter.common.vcenter.folder_manager import FolderManager
from cloudshell.cp.vcenter.common.vcenter.cancellation_service import CommandCancellationService


def orchestration_save(self, context, mode='shallow', custom_params=None):
    '\n        Creates a snapshot with a unique name and returns SavedResults as JSON\n        :param context: resource context of the vCenterShell\n        :param mode: Snapshot save mode, default shallow. Currently not it use\n        :param custom_params: Set of custom parameter to be supported in the future\n        :return: SavedResults serialized as JSON\n        :rtype: SavedResults\n        '
    resource_details = self._parse_remote_model(context)
    created_date = datetime.now()
    snapshot_name = created_date.strftime('%y_%m_%d %H_%M_%S_%f')
    created_snapshot_path = self.save_snapshot(context=context, snapshot_name=snapshot_name)
    created_snapshot_path = self._strip_double_quotes(created_snapshot_path)
    orchestration_saved_artifact = OrchestrationSavedArtifact()
    orchestration_saved_artifact.artifact_type = 'vcenter_snapshot'
    orchestration_saved_artifact.identifier = created_snapshot_path
    saved_artifacts_info = OrchestrationSavedArtifactsInfo(resource_name=resource_details.cloud_provider, created_date=created_date, restore_rules={'requires_same_resource': True}, saved_artifact=orchestration_saved_artifact)
    orchestration_save_result = OrchestrationSaveResult(saved_artifacts_info)
    return set_command_result(result=orchestration_save_result, unpicklable=False)

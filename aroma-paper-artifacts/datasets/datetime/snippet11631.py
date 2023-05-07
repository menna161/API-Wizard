from unittest import TestCase
from cloudshell.cp.core.models import DeployApp, DeployAppParams, AppResourceInfo, DeployAppDeploymentInfo, DeployAppResult
from freezegun import freeze_time
import jsonpickle
from cloudshell.api.cloudshell_api import ResourceInfo
from cloudshell.cp.vcenter.commands.command_orchestrator import CommandOrchestrator
from cloudshell.shell.core.driver_context import ResourceRemoteCommandContext, ResourceContextDetails
from cloudshell.shell.core.context import AppContext
from mock import Mock, create_autospec, patch


@freeze_time('1984-12-31 11:12:13.4567')
def test_orchestration_save_snapshot_name_should_contain_full_datetime(self):
    with patch(SAVE_SNAPSHOT) as save_snapshot_mock:
        save_snapshot_mock.return_value = '"new_snapshot"'
        remote_command_context = create_autospec(ResourceRemoteCommandContext)
        remote_command_context.resource = create_autospec(ResourceContextDetails)
        remote_command_context.resource.fullname = 'vcenter'
        endpoint = create_autospec(ResourceContextDetails)
        endpoint.fullname = 'vm_111'
        endpoint.app_context = create_autospec(AppContext)
        endpoint.app_context.deployed_app_json = '{"vmdetails": {"uid": "vm_uuid1"}}'
        remote_command_context.remote_endpoints = [endpoint]
        CommandOrchestrator().orchestration_save(context=remote_command_context, mode='shallow', custom_params=None)
        (args, kwargs) = save_snapshot_mock.call_args
        self.assertEqual(kwargs['snapshot_name'], '84_12_31 11_12_13_456700')

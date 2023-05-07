import copy
from itertools import groupby
from cloudshell.cp.core.models import ActionResultBase
from cloudshell.cp.vcenter.common.utilites.savers.artifact_saver import ArtifactHandler, UnsupportedArtifactHandler
from cloudshell.cp.vcenter.common.vcenter.task_waiter import SynchronousTaskWaiter
from cloudshell.cp.vcenter.common.vcenter.vmomi_service import pyVmomiService
import os
from multiprocessing.pool import ThreadPool


def delete_sandbox(self, si, logger, vcenter_data_model, delete_sandbox_actions, cancellation_context):
    "\n        Deletes a saved sandbox's artifacts\n\n        :param vcenter_data_model: VMwarevCenterResourceModel\n        :param vim.ServiceInstance si: py_vmomi service instance\n        :type si: vim.ServiceInstance\n        :param logger: Logger\n        :type logger: cloudshell.core.logger.qs_logger.get_qs_logger\n        :param list[SaveApp] delete_sandbox_actions:\n        :param cancellation_context:\n        "
    results = []
    logger.info(('Deleting saved sandbox command starting on ' + vcenter_data_model.default_datacenter))
    if (not delete_sandbox_actions):
        raise Exception('Failed to delete saved sandbox, missing data in request.')
    actions_grouped_by_save_types = groupby(delete_sandbox_actions, (lambda x: x.actionParams.saveDeploymentModel))
    artifactHandlersToActions = {ArtifactHandler.factory(k, self.pyvmomi_service, vcenter_data_model, si, logger, self.deployer, None, self.resource_model_parser, self.snapshot_saver, self.task_waiter, self.folder_manager, self.pg, self.cs): list(g) for (k, g) in actions_grouped_by_save_types}
    self._validate_save_deployment_models(artifactHandlersToActions, delete_sandbox_actions, results)
    error_results = [r for r in results if (not r.success)]
    if (not error_results):
        results = self._execute_delete_saved_sandbox(artifactHandlersToActions, cancellation_context, logger, results)
    return results

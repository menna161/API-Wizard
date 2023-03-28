import os
import re
import sys
from datetime import datetime, timedelta
import requests
from azure.cli.core._environment import get_config_dir
from azure.cli.core.commands import CliCommandType
from azure.cli.core.util import get_file_json
from knack.log import get_logger
from knack.util import CLIError
from six.moves import configparser
from .cli_utils import az_cli
from knack import events
from azure.cli.core._profile import ServicePrincipalAuth, _authentication_context_factory
from msrestazure.tools import parse_resource_id
from knack.arguments import CLICommandArgument
from azure.cli.core.commands.client_factory import get_mgmt_service_client
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import Deployment, DeploymentProperties
from azure.cli.core.commands import LongRunningOperation


def get_destruct_time(delta_str):
    try:
        delta = parse_time(delta_str)
        now = datetime.utcnow()
        destroy_date = (now + delta)
        return destroy_date
    except Exception:
        raise CLIError('Could not parse the time offset {}'.format(delta_str))

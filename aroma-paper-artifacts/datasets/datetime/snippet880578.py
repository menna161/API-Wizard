import re
from pydantic import validate_arguments, ValidationError
from typing_extensions import Annotated
from datetime import datetime
from pydantic import Field, StrictBool, StrictInt, StrictStr
from typing import Any, Dict, Optional
from polyaxon_sdk.models.v1_artifact_tree import V1ArtifactTree
from polyaxon_sdk.models.v1_auth import V1Auth
from polyaxon_sdk.models.v1_entities_tags import V1EntitiesTags
from polyaxon_sdk.models.v1_entities_transfer import V1EntitiesTransfer
from polyaxon_sdk.models.v1_entity_notification_body import V1EntityNotificationBody
from polyaxon_sdk.models.v1_entity_status_body_request import V1EntityStatusBodyRequest
from polyaxon_sdk.models.v1_events_response import V1EventsResponse
from polyaxon_sdk.models.v1_list_bookmarks_response import V1ListBookmarksResponse
from polyaxon_sdk.models.v1_list_run_artifacts_response import V1ListRunArtifactsResponse
from polyaxon_sdk.models.v1_list_run_connections_response import V1ListRunConnectionsResponse
from polyaxon_sdk.models.v1_list_run_edges_response import V1ListRunEdgesResponse
from polyaxon_sdk.models.v1_list_runs_response import V1ListRunsResponse
from polyaxon_sdk.models.v1_logs import V1Logs
from polyaxon_sdk.models.v1_operation_body import V1OperationBody
from polyaxon_sdk.models.v1_run import V1Run
from polyaxon_sdk.models.v1_run_artifact import V1RunArtifact
from polyaxon_sdk.models.v1_run_artifacts import V1RunArtifacts
from polyaxon_sdk.models.v1_run_settings import V1RunSettings
from polyaxon_sdk.models.v1_status import V1Status
from polyaxon_sdk.models.v1_uuids import V1Uuids
from polyaxon_sdk.api_client import ApiClient
from polyaxon_sdk.exceptions import ApiTypeError, ApiValueError


@validate_arguments
def get_run_logs(self, namespace: StrictStr, owner: Annotated[(StrictStr, Field(..., description='Owner of the namespace'))], project: Annotated[(StrictStr, Field(..., description='Project where the run will be assigned'))], uuid: Annotated[(StrictStr, Field(..., description='Uuid identifier of the entity'))], last_time: Annotated[(Optional[datetime], Field(description='last time.'))]=None, last_file: Annotated[(Optional[StrictStr], Field(description='last file.'))]=None, force: Annotated[(Optional[StrictBool], Field(description='Force query param.'))]=None, **kwargs) -> V1Logs:
    'Get run logs  # noqa: E501\n\n        This method makes a synchronous HTTP request by default. To make an\n        asynchronous HTTP request, please pass async_req=True\n\n        >>> thread = api.get_run_logs(namespace, owner, project, uuid, last_time, last_file, force, async_req=True)\n        >>> result = thread.get()\n\n        :param namespace: (required)\n        :type namespace: str\n        :param owner: Owner of the namespace (required)\n        :type owner: str\n        :param project: Project where the run will be assigned (required)\n        :type project: str\n        :param uuid: Uuid identifier of the entity (required)\n        :type uuid: str\n        :param last_time: last time.\n        :type last_time: datetime\n        :param last_file: last file.\n        :type last_file: str\n        :param force: Force query param.\n        :type force: bool\n        :param async_req: Whether to execute the request asynchronously.\n        :type async_req: bool, optional\n        :param _preload_content: if False, the urllib3.HTTPResponse object will\n                                 be returned without reading/decoding response\n                                 data. Default is True.\n        :type _preload_content: bool, optional\n        :param _request_timeout: timeout setting for this request. If one\n                                 number provided, it will be total request\n                                 timeout. It can also be a pair (tuple) of\n                                 (connection, read) timeouts.\n        :return: Returns the result object.\n                 If the method is called asynchronously,\n                 returns the request thread.\n        :rtype: V1Logs\n        '
    kwargs['_return_http_data_only'] = True
    return self.get_run_logs_with_http_info(namespace, owner, project, uuid, last_time, last_file, force, **kwargs)

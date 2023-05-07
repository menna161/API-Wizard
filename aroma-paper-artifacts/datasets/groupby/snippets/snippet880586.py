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
def get_run_stats(self, owner: Annotated[(StrictStr, Field(..., description='Owner of the namespace'))], entity: Annotated[(StrictStr, Field(..., description='Entity name under namesapce'))], uuid: Annotated[(StrictStr, Field(..., description='SubEntity uuid'))], offset: Annotated[(Optional[StrictInt], Field(description='Pagination offset.'))]=None, limit: Annotated[(Optional[StrictInt], Field(description='Limit size.'))]=None, sort: Annotated[(Optional[StrictStr], Field(description='Sort to order the search.'))]=None, query: Annotated[(Optional[StrictStr], Field(description='Query filter the search.'))]=None, bookmarks: Annotated[(Optional[StrictBool], Field(description='Filter by bookmarks.'))]=None, kind: Annotated[(Optional[StrictStr], Field(description='Stats Kind.'))]=None, aggregate: Annotated[(Optional[StrictStr], Field(description='Stats aggregate.'))]=None, groupby: Annotated[(Optional[StrictStr], Field(description='Stats group.'))]=None, trunc: Annotated[(Optional[StrictStr], Field(description='Stats trunc.'))]=None, **kwargs) -> object:
    'Get run stats  # noqa: E501\n\n        This method makes a synchronous HTTP request by default. To make an\n        asynchronous HTTP request, please pass async_req=True\n\n        >>> thread = api.get_run_stats(owner, entity, uuid, offset, limit, sort, query, bookmarks, kind, aggregate, groupby, trunc, async_req=True)\n        >>> result = thread.get()\n\n        :param owner: Owner of the namespace (required)\n        :type owner: str\n        :param entity: Entity name under namesapce (required)\n        :type entity: str\n        :param uuid: SubEntity uuid (required)\n        :type uuid: str\n        :param offset: Pagination offset.\n        :type offset: int\n        :param limit: Limit size.\n        :type limit: int\n        :param sort: Sort to order the search.\n        :type sort: str\n        :param query: Query filter the search.\n        :type query: str\n        :param bookmarks: Filter by bookmarks.\n        :type bookmarks: bool\n        :param kind: Stats Kind.\n        :type kind: str\n        :param aggregate: Stats aggregate.\n        :type aggregate: str\n        :param groupby: Stats group.\n        :type groupby: str\n        :param trunc: Stats trunc.\n        :type trunc: str\n        :param async_req: Whether to execute the request asynchronously.\n        :type async_req: bool, optional\n        :param _preload_content: if False, the urllib3.HTTPResponse object will\n                                 be returned without reading/decoding response\n                                 data. Default is True.\n        :type _preload_content: bool, optional\n        :param _request_timeout: timeout setting for this request. If one\n                                 number provided, it will be total request\n                                 timeout. It can also be a pair (tuple) of\n                                 (connection, read) timeouts.\n        :return: Returns the result object.\n                 If the method is called asynchronously,\n                 returns the request thread.\n        :rtype: object\n        '
    kwargs['_return_http_data_only'] = True
    return self.get_run_stats_with_http_info(owner, entity, uuid, offset, limit, sort, query, bookmarks, kind, aggregate, groupby, trunc, **kwargs)

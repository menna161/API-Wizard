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
def get_run_stats_with_http_info(self, owner: Annotated[(StrictStr, Field(..., description='Owner of the namespace'))], entity: Annotated[(StrictStr, Field(..., description='Entity name under namesapce'))], uuid: Annotated[(StrictStr, Field(..., description='SubEntity uuid'))], offset: Annotated[(Optional[StrictInt], Field(description='Pagination offset.'))]=None, limit: Annotated[(Optional[StrictInt], Field(description='Limit size.'))]=None, sort: Annotated[(Optional[StrictStr], Field(description='Sort to order the search.'))]=None, query: Annotated[(Optional[StrictStr], Field(description='Query filter the search.'))]=None, bookmarks: Annotated[(Optional[StrictBool], Field(description='Filter by bookmarks.'))]=None, kind: Annotated[(Optional[StrictStr], Field(description='Stats Kind.'))]=None, aggregate: Annotated[(Optional[StrictStr], Field(description='Stats aggregate.'))]=None, groupby: Annotated[(Optional[StrictStr], Field(description='Stats group.'))]=None, trunc: Annotated[(Optional[StrictStr], Field(description='Stats trunc.'))]=None, **kwargs):
    'Get run stats  # noqa: E501\n\n        This method makes a synchronous HTTP request by default. To make an\n        asynchronous HTTP request, please pass async_req=True\n\n        >>> thread = api.get_run_stats_with_http_info(owner, entity, uuid, offset, limit, sort, query, bookmarks, kind, aggregate, groupby, trunc, async_req=True)\n        >>> result = thread.get()\n\n        :param owner: Owner of the namespace (required)\n        :type owner: str\n        :param entity: Entity name under namesapce (required)\n        :type entity: str\n        :param uuid: SubEntity uuid (required)\n        :type uuid: str\n        :param offset: Pagination offset.\n        :type offset: int\n        :param limit: Limit size.\n        :type limit: int\n        :param sort: Sort to order the search.\n        :type sort: str\n        :param query: Query filter the search.\n        :type query: str\n        :param bookmarks: Filter by bookmarks.\n        :type bookmarks: bool\n        :param kind: Stats Kind.\n        :type kind: str\n        :param aggregate: Stats aggregate.\n        :type aggregate: str\n        :param groupby: Stats group.\n        :type groupby: str\n        :param trunc: Stats trunc.\n        :type trunc: str\n        :param async_req: Whether to execute the request asynchronously.\n        :type async_req: bool, optional\n        :param _return_http_data_only: response data without head status code\n                                       and headers\n        :type _return_http_data_only: bool, optional\n        :param _preload_content: if False, the urllib3.HTTPResponse object will\n                                 be returned without reading/decoding response\n                                 data. Default is True.\n        :type _preload_content: bool, optional\n        :param _request_timeout: timeout setting for this request. If one\n                                 number provided, it will be total request\n                                 timeout. It can also be a pair (tuple) of\n                                 (connection, read) timeouts.\n        :param _request_auth: set to override the auth_settings for an a single\n                              request; this effectively ignores the authentication\n                              in the spec for a single request.\n        :type _request_auth: dict, optional\n        :type _content_type: string, optional: force content-type for the request\n        :return: Returns the result object.\n                 If the method is called asynchronously,\n                 returns the request thread.\n        :rtype: tuple(object, status_code(int), headers(HTTPHeaderDict))\n        '
    _params = locals()
    _all_params = ['owner', 'entity', 'uuid', 'offset', 'limit', 'sort', 'query', 'bookmarks', 'kind', 'aggregate', 'groupby', 'trunc']
    _all_params.extend(['async_req', '_return_http_data_only', '_preload_content', '_request_timeout', '_request_auth', '_content_type', '_headers'])
    for (_key, _val) in _params['kwargs'].items():
        if (_key not in _all_params):
            raise ApiTypeError(("Got an unexpected keyword argument '%s' to method get_run_stats" % _key))
        _params[_key] = _val
    del _params['kwargs']
    _collection_formats = {}
    _path_params = {}
    if _params['owner']:
        _path_params['owner'] = _params['owner']
    if _params['entity']:
        _path_params['entity'] = _params['entity']
    if _params['uuid']:
        _path_params['uuid'] = _params['uuid']
    _query_params = []
    if (_params.get('offset') is not None):
        _query_params.append(('offset', _params['offset']))
    if (_params.get('limit') is not None):
        _query_params.append(('limit', _params['limit']))
    if (_params.get('sort') is not None):
        _query_params.append(('sort', _params['sort']))
    if (_params.get('query') is not None):
        _query_params.append(('query', _params['query']))
    if (_params.get('bookmarks') is not None):
        _query_params.append(('bookmarks', _params['bookmarks']))
    if (_params.get('kind') is not None):
        _query_params.append(('kind', _params['kind']))
    if (_params.get('aggregate') is not None):
        _query_params.append(('aggregate', _params['aggregate']))
    if (_params.get('groupby') is not None):
        _query_params.append(('groupby', _params['groupby']))
    if (_params.get('trunc') is not None):
        _query_params.append(('trunc', _params['trunc']))
    _header_params = dict(_params.get('_headers', {}))
    _form_params = []
    _files = {}
    _body_params = None
    _header_params['Accept'] = self.api_client.select_header_accept(['application/json'])
    _auth_settings = ['ApiKey']
    _response_types_map = {'200': 'object', '204': 'object', '403': 'object', '404': 'object'}
    return self.api_client.call_api('/api/v1/{owner}/{entity}/runs/{uuid}/stats', 'GET', _path_params, _query_params, _header_params, body=_body_params, post_params=_form_params, files=_files, response_types_map=_response_types_map, auth_settings=_auth_settings, async_req=_params.get('async_req'), _return_http_data_only=_params.get('_return_http_data_only'), _preload_content=_params.get('_preload_content', True), _request_timeout=_params.get('_request_timeout'), collection_formats=_collection_formats, _request_auth=_params.get('_request_auth'))

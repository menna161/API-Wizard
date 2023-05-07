import re
from pydantic import validate_arguments, ValidationError
from typing_extensions import Annotated
from pydantic import Field, StrictBool, StrictInt, StrictStr
from typing import Any, Dict, Optional
from polyaxon_sdk.models.v1_entity_stage_body_request import V1EntityStageBodyRequest
from polyaxon_sdk.models.v1_list_activities_response import V1ListActivitiesResponse
from polyaxon_sdk.models.v1_list_bookmarks_response import V1ListBookmarksResponse
from polyaxon_sdk.models.v1_list_project_versions_response import V1ListProjectVersionsResponse
from polyaxon_sdk.models.v1_list_projects_response import V1ListProjectsResponse
from polyaxon_sdk.models.v1_project import V1Project
from polyaxon_sdk.models.v1_project_settings import V1ProjectSettings
from polyaxon_sdk.models.v1_project_version import V1ProjectVersion
from polyaxon_sdk.models.v1_stage import V1Stage
from polyaxon_sdk.api_client import ApiClient
from polyaxon_sdk.exceptions import ApiTypeError, ApiValueError


@validate_arguments
def get_project_stats_with_http_info(self, owner: Annotated[(StrictStr, Field(..., description='Owner of the namespace'))], name: Annotated[(StrictStr, Field(..., description='Entity managing the resource'))], offset: Annotated[(Optional[StrictInt], Field(description='Pagination offset.'))]=None, limit: Annotated[(Optional[StrictInt], Field(description='Limit size.'))]=None, sort: Annotated[(Optional[StrictStr], Field(description='Sort to order the search.'))]=None, query: Annotated[(Optional[StrictStr], Field(description='Query filter the search.'))]=None, bookmarks: Annotated[(Optional[StrictBool], Field(description='Filter by bookmarks.'))]=None, kind: Annotated[(Optional[StrictStr], Field(description='Stats Kind.'))]=None, aggregate: Annotated[(Optional[StrictStr], Field(description='Stats aggregate.'))]=None, groupby: Annotated[(Optional[StrictStr], Field(description='Stats group.'))]=None, trunc: Annotated[(Optional[StrictStr], Field(description='Stats trunc.'))]=None, **kwargs):
    'Get project stats  # noqa: E501\n\n        This method makes a synchronous HTTP request by default. To make an\n        asynchronous HTTP request, please pass async_req=True\n\n        >>> thread = api.get_project_stats_with_http_info(owner, name, offset, limit, sort, query, bookmarks, kind, aggregate, groupby, trunc, async_req=True)\n        >>> result = thread.get()\n\n        :param owner: Owner of the namespace (required)\n        :type owner: str\n        :param name: Entity managing the resource (required)\n        :type name: str\n        :param offset: Pagination offset.\n        :type offset: int\n        :param limit: Limit size.\n        :type limit: int\n        :param sort: Sort to order the search.\n        :type sort: str\n        :param query: Query filter the search.\n        :type query: str\n        :param bookmarks: Filter by bookmarks.\n        :type bookmarks: bool\n        :param kind: Stats Kind.\n        :type kind: str\n        :param aggregate: Stats aggregate.\n        :type aggregate: str\n        :param groupby: Stats group.\n        :type groupby: str\n        :param trunc: Stats trunc.\n        :type trunc: str\n        :param async_req: Whether to execute the request asynchronously.\n        :type async_req: bool, optional\n        :param _return_http_data_only: response data without head status code\n                                       and headers\n        :type _return_http_data_only: bool, optional\n        :param _preload_content: if False, the urllib3.HTTPResponse object will\n                                 be returned without reading/decoding response\n                                 data. Default is True.\n        :type _preload_content: bool, optional\n        :param _request_timeout: timeout setting for this request. If one\n                                 number provided, it will be total request\n                                 timeout. It can also be a pair (tuple) of\n                                 (connection, read) timeouts.\n        :param _request_auth: set to override the auth_settings for an a single\n                              request; this effectively ignores the authentication\n                              in the spec for a single request.\n        :type _request_auth: dict, optional\n        :type _content_type: string, optional: force content-type for the request\n        :return: Returns the result object.\n                 If the method is called asynchronously,\n                 returns the request thread.\n        :rtype: tuple(object, status_code(int), headers(HTTPHeaderDict))\n        '
    _params = locals()
    _all_params = ['owner', 'name', 'offset', 'limit', 'sort', 'query', 'bookmarks', 'kind', 'aggregate', 'groupby', 'trunc']
    _all_params.extend(['async_req', '_return_http_data_only', '_preload_content', '_request_timeout', '_request_auth', '_content_type', '_headers'])
    for (_key, _val) in _params['kwargs'].items():
        if (_key not in _all_params):
            raise ApiTypeError(("Got an unexpected keyword argument '%s' to method get_project_stats" % _key))
        _params[_key] = _val
    del _params['kwargs']
    _collection_formats = {}
    _path_params = {}
    if _params['owner']:
        _path_params['owner'] = _params['owner']
    if _params['name']:
        _path_params['name'] = _params['name']
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
    return self.api_client.call_api('/api/v1/{owner}/{name}/stats', 'GET', _path_params, _query_params, _header_params, body=_body_params, post_params=_form_params, files=_files, response_types_map=_response_types_map, auth_settings=_auth_settings, async_req=_params.get('async_req'), _return_http_data_only=_params.get('_return_http_data_only'), _preload_content=_params.get('_preload_content', True), _request_timeout=_params.get('_request_timeout'), collection_formats=_collection_formats, _request_auth=_params.get('_request_auth'))

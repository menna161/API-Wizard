import re
from pydantic import validate_arguments, ValidationError
from typing_extensions import Annotated
from datetime import datetime
from pydantic import Field, StrictBool, StrictInt, StrictStr
from typing import Any, Dict, Optional
from polyaxon_sdk.models.v1_entities_tags import V1EntitiesTags
from polyaxon_sdk.models.v1_entities_transfer import V1EntitiesTransfer
from polyaxon_sdk.models.v1_list_activities_response import V1ListActivitiesResponse
from polyaxon_sdk.models.v1_list_organization_members_response import V1ListOrganizationMembersResponse
from polyaxon_sdk.models.v1_list_organizations_response import V1ListOrganizationsResponse
from polyaxon_sdk.models.v1_list_runs_response import V1ListRunsResponse
from polyaxon_sdk.models.v1_organization import V1Organization
from polyaxon_sdk.models.v1_organization_member import V1OrganizationMember
from polyaxon_sdk.models.v1_run import V1Run
from polyaxon_sdk.models.v1_uuids import V1Uuids
from polyaxon_sdk.api_client import ApiClient
from polyaxon_sdk.exceptions import ApiTypeError, ApiValueError


@validate_arguments
def get_organization_settings_with_http_info(self, owner: Annotated[(StrictStr, Field(..., description='Owner of the namespace'))], organization_user: Annotated[(Optional[StrictStr], Field(description='User.'))]=None, organization_user_email: Annotated[(Optional[StrictStr], Field(description='Read-only User email.'))]=None, organization_name: Annotated[(Optional[StrictStr], Field(description='Name.'))]=None, organization_is_public: Annotated[(Optional[StrictBool], Field(description='Optional flag to tell if this organization is public.'))]=None, organization_created_at: Annotated[(Optional[datetime], Field(description='Optional time when the entity was created.'))]=None, organization_updated_at: Annotated[(Optional[datetime], Field(description='Optional last time the entity was updated.'))]=None, organization_support_revoke_at: Annotated[(Optional[datetime], Field(description='Optional time to revoke support access.'))]=None, organization_expiration: Annotated[(Optional[StrictInt], Field(description='Optional expiration for support.'))]=None, organization_role: Annotated[(Optional[StrictStr], Field(description="Current user's role in this org."))]=None, organization_queue: Annotated[(Optional[StrictStr], Field(description='Default queue.'))]=None, organization_preset: Annotated[(Optional[StrictStr], Field(description='Default preset.'))]=None, organization_is_cloud_viewable: Annotated[(Optional[StrictBool], Field(description='Setting to enable viewable metadata on cloud.'))]=None, **kwargs):
    "Get organization settings  # noqa: E501\n\n        This method makes a synchronous HTTP request by default. To make an\n        asynchronous HTTP request, please pass async_req=True\n\n        >>> thread = api.get_organization_settings_with_http_info(owner, organization_user, organization_user_email, organization_name, organization_is_public, organization_created_at, organization_updated_at, organization_support_revoke_at, organization_expiration, organization_role, organization_queue, organization_preset, organization_is_cloud_viewable, async_req=True)\n        >>> result = thread.get()\n\n        :param owner: Owner of the namespace (required)\n        :type owner: str\n        :param organization_user: User.\n        :type organization_user: str\n        :param organization_user_email: Read-only User email.\n        :type organization_user_email: str\n        :param organization_name: Name.\n        :type organization_name: str\n        :param organization_is_public: Optional flag to tell if this organization is public.\n        :type organization_is_public: bool\n        :param organization_created_at: Optional time when the entity was created.\n        :type organization_created_at: datetime\n        :param organization_updated_at: Optional last time the entity was updated.\n        :type organization_updated_at: datetime\n        :param organization_support_revoke_at: Optional time to revoke support access.\n        :type organization_support_revoke_at: datetime\n        :param organization_expiration: Optional expiration for support.\n        :type organization_expiration: int\n        :param organization_role: Current user's role in this org.\n        :type organization_role: str\n        :param organization_queue: Default queue.\n        :type organization_queue: str\n        :param organization_preset: Default preset.\n        :type organization_preset: str\n        :param organization_is_cloud_viewable: Setting to enable viewable metadata on cloud.\n        :type organization_is_cloud_viewable: bool\n        :param async_req: Whether to execute the request asynchronously.\n        :type async_req: bool, optional\n        :param _return_http_data_only: response data without head status code\n                                       and headers\n        :type _return_http_data_only: bool, optional\n        :param _preload_content: if False, the urllib3.HTTPResponse object will\n                                 be returned without reading/decoding response\n                                 data. Default is True.\n        :type _preload_content: bool, optional\n        :param _request_timeout: timeout setting for this request. If one\n                                 number provided, it will be total request\n                                 timeout. It can also be a pair (tuple) of\n                                 (connection, read) timeouts.\n        :param _request_auth: set to override the auth_settings for an a single\n                              request; this effectively ignores the authentication\n                              in the spec for a single request.\n        :type _request_auth: dict, optional\n        :type _content_type: string, optional: force content-type for the request\n        :return: Returns the result object.\n                 If the method is called asynchronously,\n                 returns the request thread.\n        :rtype: tuple(V1Organization, status_code(int), headers(HTTPHeaderDict))\n        "
    _params = locals()
    _all_params = ['owner', 'organization_user', 'organization_user_email', 'organization_name', 'organization_is_public', 'organization_created_at', 'organization_updated_at', 'organization_support_revoke_at', 'organization_expiration', 'organization_role', 'organization_queue', 'organization_preset', 'organization_is_cloud_viewable']
    _all_params.extend(['async_req', '_return_http_data_only', '_preload_content', '_request_timeout', '_request_auth', '_content_type', '_headers'])
    for (_key, _val) in _params['kwargs'].items():
        if (_key not in _all_params):
            raise ApiTypeError(("Got an unexpected keyword argument '%s' to method get_organization_settings" % _key))
        _params[_key] = _val
    del _params['kwargs']
    _collection_formats = {}
    _path_params = {}
    if _params['owner']:
        _path_params['owner'] = _params['owner']
    _query_params = []
    if (_params.get('organization_user') is not None):
        _query_params.append(('organization.user', _params['organization_user']))
    if (_params.get('organization_user_email') is not None):
        _query_params.append(('organization.user_email', _params['organization_user_email']))
    if (_params.get('organization_name') is not None):
        _query_params.append(('organization.name', _params['organization_name']))
    if (_params.get('organization_is_public') is not None):
        _query_params.append(('organization.is_public', _params['organization_is_public']))
    if (_params.get('organization_created_at') is not None):
        if isinstance(_params['organization_created_at'], datetime):
            _query_params.append(('organization.created_at', _params['organization_created_at'].strftime(self.api_client.configuration.datetime_format)))
        else:
            _query_params.append(('organization.created_at', _params['organization_created_at']))
    if (_params.get('organization_updated_at') is not None):
        if isinstance(_params['organization_updated_at'], datetime):
            _query_params.append(('organization.updated_at', _params['organization_updated_at'].strftime(self.api_client.configuration.datetime_format)))
        else:
            _query_params.append(('organization.updated_at', _params['organization_updated_at']))
    if (_params.get('organization_support_revoke_at') is not None):
        if isinstance(_params['organization_support_revoke_at'], datetime):
            _query_params.append(('organization.support_revoke_at', _params['organization_support_revoke_at'].strftime(self.api_client.configuration.datetime_format)))
        else:
            _query_params.append(('organization.support_revoke_at', _params['organization_support_revoke_at']))
    if (_params.get('organization_expiration') is not None):
        _query_params.append(('organization.expiration', _params['organization_expiration']))
    if (_params.get('organization_role') is not None):
        _query_params.append(('organization.role', _params['organization_role']))
    if (_params.get('organization_queue') is not None):
        _query_params.append(('organization.queue', _params['organization_queue']))
    if (_params.get('organization_preset') is not None):
        _query_params.append(('organization.preset', _params['organization_preset']))
    if (_params.get('organization_is_cloud_viewable') is not None):
        _query_params.append(('organization.is_cloud_viewable', _params['organization_is_cloud_viewable']))
    _header_params = dict(_params.get('_headers', {}))
    _form_params = []
    _files = {}
    _body_params = None
    _header_params['Accept'] = self.api_client.select_header_accept(['application/json'])
    _auth_settings = ['ApiKey']
    _response_types_map = {'200': 'V1Organization', '204': 'object', '403': 'object', '404': 'object'}
    return self.api_client.call_api('/api/v1/orgs/{owner}/settings', 'GET', _path_params, _query_params, _header_params, body=_body_params, post_params=_form_params, files=_files, response_types_map=_response_types_map, auth_settings=_auth_settings, async_req=_params.get('async_req'), _return_http_data_only=_params.get('_return_http_data_only'), _preload_content=_params.get('_preload_content', True), _request_timeout=_params.get('_request_timeout'), collection_formats=_collection_formats, _request_auth=_params.get('_request_auth'))

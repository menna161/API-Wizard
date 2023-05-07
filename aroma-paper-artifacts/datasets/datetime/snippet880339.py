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
def get_organization_invitation_with_http_info(self, owner: Annotated[(StrictStr, Field(..., description='Owner of the namespace'))], member_user: Annotated[(Optional[StrictStr], Field(description='User.'))]=None, member_user_email: Annotated[(Optional[StrictStr], Field(description='Read-only User email.'))]=None, member_role: Annotated[(Optional[StrictStr], Field(description='Role.'))]=None, member_kind: Annotated[(Optional[StrictStr], Field(description='Kind.'))]=None, member_created_at: Annotated[(Optional[datetime], Field(description='Optional time when the entity was created.'))]=None, member_updated_at: Annotated[(Optional[datetime], Field(description='Optional last time the entity was updated.'))]=None, email: Annotated[(Optional[StrictStr], Field(description='Optional email.'))]=None, **kwargs):
    'Get organization invitation details  # noqa: E501\n\n        This method makes a synchronous HTTP request by default. To make an\n        asynchronous HTTP request, please pass async_req=True\n\n        >>> thread = api.get_organization_invitation_with_http_info(owner, member_user, member_user_email, member_role, member_kind, member_created_at, member_updated_at, email, async_req=True)\n        >>> result = thread.get()\n\n        :param owner: Owner of the namespace (required)\n        :type owner: str\n        :param member_user: User.\n        :type member_user: str\n        :param member_user_email: Read-only User email.\n        :type member_user_email: str\n        :param member_role: Role.\n        :type member_role: str\n        :param member_kind: Kind.\n        :type member_kind: str\n        :param member_created_at: Optional time when the entity was created.\n        :type member_created_at: datetime\n        :param member_updated_at: Optional last time the entity was updated.\n        :type member_updated_at: datetime\n        :param email: Optional email.\n        :type email: str\n        :param async_req: Whether to execute the request asynchronously.\n        :type async_req: bool, optional\n        :param _return_http_data_only: response data without head status code\n                                       and headers\n        :type _return_http_data_only: bool, optional\n        :param _preload_content: if False, the urllib3.HTTPResponse object will\n                                 be returned without reading/decoding response\n                                 data. Default is True.\n        :type _preload_content: bool, optional\n        :param _request_timeout: timeout setting for this request. If one\n                                 number provided, it will be total request\n                                 timeout. It can also be a pair (tuple) of\n                                 (connection, read) timeouts.\n        :param _request_auth: set to override the auth_settings for an a single\n                              request; this effectively ignores the authentication\n                              in the spec for a single request.\n        :type _request_auth: dict, optional\n        :type _content_type: string, optional: force content-type for the request\n        :return: Returns the result object.\n                 If the method is called asynchronously,\n                 returns the request thread.\n        :rtype: tuple(V1OrganizationMember, status_code(int), headers(HTTPHeaderDict))\n        '
    _params = locals()
    _all_params = ['owner', 'member_user', 'member_user_email', 'member_role', 'member_kind', 'member_created_at', 'member_updated_at', 'email']
    _all_params.extend(['async_req', '_return_http_data_only', '_preload_content', '_request_timeout', '_request_auth', '_content_type', '_headers'])
    for (_key, _val) in _params['kwargs'].items():
        if (_key not in _all_params):
            raise ApiTypeError(("Got an unexpected keyword argument '%s' to method get_organization_invitation" % _key))
        _params[_key] = _val
    del _params['kwargs']
    _collection_formats = {}
    _path_params = {}
    if _params['owner']:
        _path_params['owner'] = _params['owner']
    _query_params = []
    if (_params.get('member_user') is not None):
        _query_params.append(('member.user', _params['member_user']))
    if (_params.get('member_user_email') is not None):
        _query_params.append(('member.user_email', _params['member_user_email']))
    if (_params.get('member_role') is not None):
        _query_params.append(('member.role', _params['member_role']))
    if (_params.get('member_kind') is not None):
        _query_params.append(('member.kind', _params['member_kind']))
    if (_params.get('member_created_at') is not None):
        if isinstance(_params['member_created_at'], datetime):
            _query_params.append(('member.created_at', _params['member_created_at'].strftime(self.api_client.configuration.datetime_format)))
        else:
            _query_params.append(('member.created_at', _params['member_created_at']))
    if (_params.get('member_updated_at') is not None):
        if isinstance(_params['member_updated_at'], datetime):
            _query_params.append(('member.updated_at', _params['member_updated_at'].strftime(self.api_client.configuration.datetime_format)))
        else:
            _query_params.append(('member.updated_at', _params['member_updated_at']))
    if (_params.get('email') is not None):
        _query_params.append(('email', _params['email']))
    _header_params = dict(_params.get('_headers', {}))
    _form_params = []
    _files = {}
    _body_params = None
    _header_params['Accept'] = self.api_client.select_header_accept(['application/json'])
    _auth_settings = ['ApiKey']
    _response_types_map = {'200': 'V1OrganizationMember', '204': 'object', '403': 'object', '404': 'object'}
    return self.api_client.call_api('/api/v1/orgs/{owner}/invitations', 'GET', _path_params, _query_params, _header_params, body=_body_params, post_params=_form_params, files=_files, response_types_map=_response_types_map, auth_settings=_auth_settings, async_req=_params.get('async_req'), _return_http_data_only=_params.get('_return_http_data_only'), _preload_content=_params.get('_preload_content', True), _request_timeout=_params.get('_request_timeout'), collection_formats=_collection_formats, _request_auth=_params.get('_request_auth'))

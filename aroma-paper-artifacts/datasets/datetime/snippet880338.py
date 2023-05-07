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
def get_organization_invitation(self, owner: Annotated[(StrictStr, Field(..., description='Owner of the namespace'))], member_user: Annotated[(Optional[StrictStr], Field(description='User.'))]=None, member_user_email: Annotated[(Optional[StrictStr], Field(description='Read-only User email.'))]=None, member_role: Annotated[(Optional[StrictStr], Field(description='Role.'))]=None, member_kind: Annotated[(Optional[StrictStr], Field(description='Kind.'))]=None, member_created_at: Annotated[(Optional[datetime], Field(description='Optional time when the entity was created.'))]=None, member_updated_at: Annotated[(Optional[datetime], Field(description='Optional last time the entity was updated.'))]=None, email: Annotated[(Optional[StrictStr], Field(description='Optional email.'))]=None, **kwargs) -> V1OrganizationMember:
    'Get organization invitation details  # noqa: E501\n\n        This method makes a synchronous HTTP request by default. To make an\n        asynchronous HTTP request, please pass async_req=True\n\n        >>> thread = api.get_organization_invitation(owner, member_user, member_user_email, member_role, member_kind, member_created_at, member_updated_at, email, async_req=True)\n        >>> result = thread.get()\n\n        :param owner: Owner of the namespace (required)\n        :type owner: str\n        :param member_user: User.\n        :type member_user: str\n        :param member_user_email: Read-only User email.\n        :type member_user_email: str\n        :param member_role: Role.\n        :type member_role: str\n        :param member_kind: Kind.\n        :type member_kind: str\n        :param member_created_at: Optional time when the entity was created.\n        :type member_created_at: datetime\n        :param member_updated_at: Optional last time the entity was updated.\n        :type member_updated_at: datetime\n        :param email: Optional email.\n        :type email: str\n        :param async_req: Whether to execute the request asynchronously.\n        :type async_req: bool, optional\n        :param _preload_content: if False, the urllib3.HTTPResponse object will\n                                 be returned without reading/decoding response\n                                 data. Default is True.\n        :type _preload_content: bool, optional\n        :param _request_timeout: timeout setting for this request. If one\n                                 number provided, it will be total request\n                                 timeout. It can also be a pair (tuple) of\n                                 (connection, read) timeouts.\n        :return: Returns the result object.\n                 If the method is called asynchronously,\n                 returns the request thread.\n        :rtype: V1OrganizationMember\n        '
    kwargs['_return_http_data_only'] = True
    return self.get_organization_invitation_with_http_info(owner, member_user, member_user_email, member_role, member_kind, member_created_at, member_updated_at, email, **kwargs)

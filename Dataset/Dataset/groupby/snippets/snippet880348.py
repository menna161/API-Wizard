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
def get_organization_stats(self, owner: Annotated[(StrictStr, Field(..., description='Owner of the namespace'))], offset: Annotated[(Optional[StrictInt], Field(description='Pagination offset.'))]=None, limit: Annotated[(Optional[StrictInt], Field(description='Limit size.'))]=None, sort: Annotated[(Optional[StrictStr], Field(description='Sort to order the search.'))]=None, query: Annotated[(Optional[StrictStr], Field(description='Query filter the search.'))]=None, bookmarks: Annotated[(Optional[StrictBool], Field(description='Filter by bookmarks.'))]=None, kind: Annotated[(Optional[StrictStr], Field(description='Stats Kind.'))]=None, aggregate: Annotated[(Optional[StrictStr], Field(description='Stats aggregate.'))]=None, groupby: Annotated[(Optional[StrictStr], Field(description='Stats group.'))]=None, trunc: Annotated[(Optional[StrictStr], Field(description='Stats trunc.'))]=None, **kwargs) -> object:
    'Get organization stats  # noqa: E501\n\n        This method makes a synchronous HTTP request by default. To make an\n        asynchronous HTTP request, please pass async_req=True\n\n        >>> thread = api.get_organization_stats(owner, offset, limit, sort, query, bookmarks, kind, aggregate, groupby, trunc, async_req=True)\n        >>> result = thread.get()\n\n        :param owner: Owner of the namespace (required)\n        :type owner: str\n        :param offset: Pagination offset.\n        :type offset: int\n        :param limit: Limit size.\n        :type limit: int\n        :param sort: Sort to order the search.\n        :type sort: str\n        :param query: Query filter the search.\n        :type query: str\n        :param bookmarks: Filter by bookmarks.\n        :type bookmarks: bool\n        :param kind: Stats Kind.\n        :type kind: str\n        :param aggregate: Stats aggregate.\n        :type aggregate: str\n        :param groupby: Stats group.\n        :type groupby: str\n        :param trunc: Stats trunc.\n        :type trunc: str\n        :param async_req: Whether to execute the request asynchronously.\n        :type async_req: bool, optional\n        :param _preload_content: if False, the urllib3.HTTPResponse object will\n                                 be returned without reading/decoding response\n                                 data. Default is True.\n        :type _preload_content: bool, optional\n        :param _request_timeout: timeout setting for this request. If one\n                                 number provided, it will be total request\n                                 timeout. It can also be a pair (tuple) of\n                                 (connection, read) timeouts.\n        :return: Returns the result object.\n                 If the method is called asynchronously,\n                 returns the request thread.\n        :rtype: object\n        '
    kwargs['_return_http_data_only'] = True
    return self.get_organization_stats_with_http_info(owner, offset, limit, sort, query, bookmarks, kind, aggregate, groupby, trunc, **kwargs)

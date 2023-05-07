import logging
from typing import Any, Optional, Union
from chromewhip.helpers import PayloadMixin, BaseEvent, ChromeTypeBase
from chromewhip.protocol import runtime as Runtime


@classmethod
def getBoxModel(cls, nodeId: Optional['NodeId']=None, backendNodeId: Optional['BackendNodeId']=None, objectId: Optional['Runtime.RemoteObjectId']=None):
    'Returns boxes for the given node.\n        :param nodeId: Identifier of the node.\n        :type nodeId: NodeId\n        :param backendNodeId: Identifier of the backend node.\n        :type backendNodeId: BackendNodeId\n        :param objectId: JavaScript object id of the node wrapper.\n        :type objectId: Runtime.RemoteObjectId\n        '
    return (cls.build_send_payload('getBoxModel', {'nodeId': nodeId, 'backendNodeId': backendNodeId, 'objectId': objectId}), cls.convert_payload({'model': {'class': BoxModel, 'optional': False}}))

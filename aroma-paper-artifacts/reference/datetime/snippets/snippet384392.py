import datetime
import json
import logging
import requests


def add(self, index_name=None, doc_type=None, index_id=None, json_message=None):
    "\n            Returns the id of the newly inserted value or None\n            if the added date is not there, then I'm adding it in\n        "
    if (not isinstance(json_message, dict)):
        json_message_dict = json.loads(json_message)
    else:
        json_message_dict = json_message
    json_message_dict['addedIso'] = datetime.datetime.now().isoformat()
    json_message_dict['updatedIso'] = json_message_dict['addedIso']
    json_message = json.dumps(json_message_dict)
    self.log.info(('adding item into ES: ' + str(json_message_dict)))
    if index_id:
        response = requests.put(((((((self.connections + '/') + index_name) + '/') + doc_type) + '/') + index_id), data=json_message)
    else:
        response = requests.post(((((self.connections + '/') + index_name) + '/') + doc_type), data=json_message)
    self.log.info(((('response: ' + str(response.content)) + '...message: ') + str(response.content)))
    responseid = None
    try:
        responseid = json.loads(response.content).get('_id')
    except Exception:
        pass
    return responseid

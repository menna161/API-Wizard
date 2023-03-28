import logging
from lxml import etree
from lxml.builder import ElementMaker
from datetime import datetime
from pytz import utc
from ..exceptions import FailedExchangeException


def _xpath_to_dict(self, element, property_map, namespace_map):
    "\n    property_map = {\n      u'name'         : { u'xpath' : u't:Mailbox/t:Name'},\n      u'email'        : { u'xpath' : u't:Mailbox/t:EmailAddress'},\n      u'response'     : { u'xpath' : u't:ResponseType'},\n      u'last_response': { u'xpath' : u't:LastResponseTime', u'cast': u'datetime'},\n    }\n\n    This runs the given xpath on the node and returns a dictionary\n\n    "
    result = {}
    log.info(etree.tostring(element, pretty_print=True))
    for key in property_map:
        item = property_map[key]
        log.info(u'Pulling xpath {xpath} into key {key}'.format(key=key, xpath=item[u'xpath']))
        nodes = element.xpath(item[u'xpath'], namespaces=namespace_map)
        if nodes:
            result_for_node = []
            for node in nodes:
                cast_as = item.get(u'cast', None)
                if (cast_as == u'datetime'):
                    result_for_node.append(self._parse_date(node.text))
                elif (cast_as == u'date_only_naive'):
                    result_for_node.append(self._parse_date_only_naive(node.text))
                elif (cast_as == u'int'):
                    result_for_node.append(int(node.text))
                elif (cast_as == u'bool'):
                    if (node.text.lower() == u'true'):
                        result_for_node.append(True)
                    else:
                        result_for_node.append(False)
                else:
                    result_for_node.append(node.text)
            if (not result_for_node):
                result[key] = None
            elif (len(result_for_node) == 1):
                result[key] = result_for_node[0]
            else:
                result[key] = result_for_node
    return result

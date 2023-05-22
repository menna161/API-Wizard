import json
import re
import gzip
import pprint
import requests
from axcell import config


def gql(query, **variables):
    query = {'query': query}
    r = requests.post(url=config.graphql_url, json=query)
    return json.loads(r.text)

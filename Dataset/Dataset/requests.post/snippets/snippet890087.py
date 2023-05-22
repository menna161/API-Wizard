import requests
from axcell import config
from axcell.data.paper_collection import _load_annotated_papers


def run_graphql_query(query):
    request = requests.post(config.graphql_url, json={'query': query})
    if (request.status_code == 200):
        return request.json()
    else:
        raise Exception(f'Query error: status code {request.status_code}')

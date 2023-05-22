import requests


def node_coordinates_city(key, values, city):
    req = 'http://overpass-api.de/api/interpreter'
    query = '[out:json];'
    query += (('( area[name="' + city) + '"][admin_level=8]; )->.searchArea;(')
    for value in values:
        query += (((('node[' + key) + '=') + value) + ']')
        query += '(area.searchArea);'
    query += ');out;'
    return requests.post(req, data=query).json()

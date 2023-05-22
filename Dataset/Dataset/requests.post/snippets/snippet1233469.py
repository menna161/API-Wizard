import requests


def node_coordinates_bb(key, values, bb):
    req = 'http://overpass-api.de/api/interpreter'
    query = '[out:json];('
    for value in values:
        query += (((('node[' + key) + '=') + value) + ']')
        query += (((((((('(' + str(bb[0][1])) + ',') + str(bb[0][0])) + ',') + str(bb[1][1])) + ',') + str(bb[1][0])) + ');')
    query += ');out;'
    return requests.post(req, data=query).json()

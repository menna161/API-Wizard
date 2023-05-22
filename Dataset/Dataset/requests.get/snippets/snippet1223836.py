import os
from flask import Flask, abort, jsonify, request
from icalendar import Calendar
import requests


@app.route('/<path:url>')
def convert_from_url(url):
    if (url == 'favicon.ico'):
        abort(404)
    if (not url.startswith('http')):
        url = ('http://%s' % url)
    try:
        r = requests.get(url)
    except:
        abort(500)
    if (not r.ok):
        abort(r.status_code)
    ics = r.content
    cal = Calendar.from_ical(ics)
    data = {}
    data[cal.name] = dict(cal.items())
    for component in cal.subcomponents:
        if (not (component.name in data[cal.name])):
            data[cal.name][component.name] = []
        comp_obj = {}
        for item in component.items():
            if hasattr(item[1], 'dt'):
                val = item[1].dt.isoformat()
            else:
                val = item[1].to_ical().decode('utf-8').replace('\\,', ',')
            comp_obj[item[0]] = val
        data[cal.name][component.name].append(comp_obj)
    resp = jsonify(data)
    if ('callback' in request.args):
        resp.data = ('%s(%s);' % (request.args['callback'], resp.data))
    return resp

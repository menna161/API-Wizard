import logging
import os
import os.path
from typing import Any, Dict
import cherrypy
from flask import Blueprint, current_app, Flask, jsonify, render_template, request, session
from flask_caching import Cache
from flask_talisman import Talisman, GOOGLE_CSP_POLICY
import opentracing
from flask_opentracing import FlaskTracer
from jaeger_client import Config
from prometheus_flask_exporter import PrometheusMetrics
from requestlogger import ApacheFormatter, WSGILogger
import requests
from werkzeug.contrib.fixers import ProxyFix


@superpower.route('/')
def index():
    with requests.Session() as req_session:
        parent_span = tracer.get_span(request)
        powerservice_url = current_app.config['POWERSOURCE_URL']
        cid = session.get('cid')
        if (cid is None):
            r = req_session.get('{}/random'.format(powerservice_url), timeout=(2, 2))
            cid = r.json()['character_id']
            session['cid'] = cid
        headers = {'Connection': 'close'}
        t = opentracing.tracer
        with t.start_span('fetch character', child_of=parent_span) as span:
            url = '{}/{}'.format(powerservice_url, cid)
            span.set_tag('http.method', 'GET')
            span.set_tag('http.url', url)
            span.set_tag('span.kind', 'client')
            t.inject(span, opentracing.Format.HTTP_HEADERS, headers)
            info = req_session.get(url, headers=headers, timeout=(5, 2)).json()
        accept = request.headers.get('Accept')
        if (accept == 'application/json'):
            return jsonify(info)
        return render_template('index.html', name=info['name'], description=info['description'], img_url=info['img_url'], learn_more_url=info['learn_more_url'])

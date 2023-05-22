from flask import Flask, render_template, redirect, url_for, request, make_response
from pymongo import MongoClient
from bson.objectid import ObjectId
import socket
import os
import json


@app.route('/api/rsvps', methods=['GET', 'POST'])
def api_rsvps():
    if (request.method == 'GET'):
        docs = [rsvp.dict() for rsvp in RSVP.find_all()]
        return json.dumps(docs, indent=True)
    else:
        try:
            doc = json.loads(request.data)
        except ValueError:
            return ('{"error": "expecting JSON payload"}', 400)
        if ('name' not in doc):
            return ('{"error": "name field is missing"}', 400)
        if ('email' not in doc):
            return ('{"error": "email field is missing"}', 400)
        rsvp = RSVP.new(name=doc['name'], email=doc['email'])
        return json.dumps(rsvp.dict(), indent=True)

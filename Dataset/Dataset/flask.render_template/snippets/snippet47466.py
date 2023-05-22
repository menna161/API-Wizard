import os
import json
import flask
from flask import Flask, request
import datetime


@app.route('/regid/<reg_id>')
def feedback_form(reg_id):
    try:
        data = [d for d in mind_match_data if (d['registrant_id'] == int(reg_id))][0]
        for match in data['matches_info']:
            match.pop('registrant_id', None)
        data.update({'enumerate': enumerate})
    except:
        data = {'registrant_id': 0, 'full_name': 'John Doe', 'email': 'john_doe@gmail.com', 'affiliation': 'Random University', 'matches_info': [], 'enumerate': enumerate}
    return flask.render_template('feedback.html', **data)

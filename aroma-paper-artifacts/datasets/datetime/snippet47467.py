import os
import json
import flask
from flask import Flask, request
import datetime


@app.route('/handle_submit/', methods=['GET', 'POST'])
def handle_submit():
    if (request.method == 'POST'):
        print(request.form)
        feedback_data = read_json(FEEDBACK_DATA_PATH)
        registrant_id = request.form['registrant_id']
        feedback_text = request.form.get('text_input', '')
        relevances = [request.form.get(('relevance_%s' % i), '0') for i in range(0, 6)]
        satisfactory = [request.form.get(('satisfactory_%s' % i), '0') for i in range(0, 6)]
        coi = [request.form.get(('coi_%s' % i), '0') for i in range(0, 6)]
        arrange_before = request.form.get('before_checkbox', '0')
        useful = request.form.get('useful', '0')
        enjoyable = request.form.get('enjoyable', '0')
        feedback_data.append({'registrant_id': registrant_id, 'relevances': relevances, 'satisfactory': satisfactory, 'coi': coi, 'feedback_text': feedback_text, 'arrange_before': arrange_before, 'useful': useful, 'enjoyable': enjoyable, 'timestamp': str(datetime.datetime.now())})
        save_json(feedback_data, FEEDBACK_DATA_PATH)
    return flask.redirect('/')

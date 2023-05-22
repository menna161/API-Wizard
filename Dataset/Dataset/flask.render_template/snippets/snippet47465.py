import os
import json
import flask
from flask import Flask, request
import datetime


@app.route('/', methods=['GET', 'POST'])
def index():
    return flask.render_template('index.html')

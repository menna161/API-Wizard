import os
import json
import dateutil.parser
import pytest
import flask
import unicodecsv
import sqlalchemy
import babbage.api
import babbage.model
import babbage.manager


@pytest.fixture()
def app():
    app = flask.Flask('test')
    app.register_blueprint(babbage.api.blueprint, url_prefix='/bbg')
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True
    return app

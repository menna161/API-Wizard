import os
import unittest
import flask
import flask_pymongo


def setUp(self):
    super(FlaskRequestTest, self).setUp()
    self.dbname = self.__class__.__name__
    self.app = flask.Flask('test')
    self.context = self.app.test_request_context('/')
    self.context.push()

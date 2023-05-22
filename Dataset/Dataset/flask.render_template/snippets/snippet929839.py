import os
import time
import cPickle
import datetime
import logging
import flask
import werkzeug
import optparse
import tornado.wsgi
import tornado.httpserver
import numpy as np
import pandas as pd
from PIL import Image
import cStringIO as StringIO
import urllib
import exifutil
import caffe


@app.route('/classify_url', methods=['GET'])
def classify_url():
    imageurl = flask.request.args.get('imageurl', '')
    try:
        string_buffer = StringIO.StringIO(urllib.urlopen(imageurl).read())
        image = caffe.io.load_image(string_buffer)
    except Exception as err:
        logging.info('URL Image open error: %s', err)
        return flask.render_template('index.html', has_result=True, result=(False, 'Cannot open image from URL.'))
    logging.info('Image: %s', imageurl)
    result = app.clf.classify_image(image)
    return flask.render_template('index.html', has_result=True, result=result, imagesrc=imageurl)

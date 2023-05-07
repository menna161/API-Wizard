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


@app.route('/classify_upload', methods=['POST'])
def classify_upload():
    try:
        imagefile = flask.request.files['imagefile']
        filename_ = (str(datetime.datetime.now()).replace(' ', '_') + werkzeug.secure_filename(imagefile.filename))
        filename = os.path.join(UPLOAD_FOLDER, filename_)
        imagefile.save(filename)
        logging.info('Saving to %s.', filename)
        image = exifutil.open_oriented_im(filename)
    except Exception as err:
        logging.info('Uploaded image open error: %s', err)
        return flask.render_template('index.html', has_result=True, result=(False, 'Cannot open uploaded image.'))
    result = app.clf.classify_image(image)
    return flask.render_template('index.html', has_result=True, result=result, imagesrc=embed_image_html(image))

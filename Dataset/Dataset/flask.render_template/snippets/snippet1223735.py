import flask
from collections import namedtuple
import datetime
import re


@app.route('/blackvue_vod.cgi', methods=['GET'])
def vod():
    'returns the index of recordings'
    filenames = [filename for filename in generate_recording_filenames()]
    return flask.render_template('vod.txt', filenames=filenames)

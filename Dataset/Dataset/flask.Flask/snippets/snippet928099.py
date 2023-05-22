from functools import partial
from mimetypes import guess_type
from flask import abort, current_app, request
from gridfs import GridFS, NoFile
from pymongo import uri_parser
from werkzeug.wsgi import wrap_file
import pymongo
from flask_pymongo.helpers import BSONObjectIdConverter, JSONEncoder
from flask_pymongo.wrappers import MongoClient


def send_file(self, filename, base='fs', version=(- 1), cache_for=31536000):
    'Respond with a file from GridFS.\n\n        Returns an instance of the :attr:`~flask.Flask.response_class`\n        containing the named file, and implement conditional GET semantics\n        (using :meth:`~werkzeug.wrappers.ETagResponseMixin.make_conditional`).\n\n        .. code-block:: python\n\n            @app.route("/uploads/<path:filename>")\n            def get_upload(filename):\n                return mongo.send_file(filename)\n\n        :param str filename: the filename of the file to return\n        :param str base: the base name of the GridFS collections to use\n        :param bool version: if positive, return the Nth revision of the file\n           identified by filename; if negative, return the Nth most recent\n           revision. If no such version exists, return with HTTP status 404.\n        :param int cache_for: number of seconds that browsers should be\n           instructed to cache responses\n        '
    if (not isinstance(base, str)):
        raise TypeError("'base' must be string or unicode")
    if (not isinstance(version, int)):
        raise TypeError("'version' must be an integer")
    if (not isinstance(cache_for, int)):
        raise TypeError("'cache_for' must be an integer")
    storage = GridFS(self.db, base)
    try:
        fileobj = storage.get_version(filename=filename, version=version)
    except NoFile:
        abort(404)
    data = wrap_file(request.environ, fileobj, buffer_size=(1024 * 255))
    response = current_app.response_class(data, mimetype=fileobj.content_type, direct_passthrough=True)
    response.content_length = fileobj.length
    response.last_modified = fileobj.upload_date
    response.set_etag(fileobj.md5)
    response.cache_control.max_age = cache_for
    response.cache_control.public = True
    response.make_conditional(request)
    return response

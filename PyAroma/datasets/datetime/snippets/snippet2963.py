import csv
from datetime import datetime
from io import StringIO
from jinja2 import Environment, PackageLoader
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response
from .tools import apply_filters


def compute_csv(urls, filters, excludes):
    'Generate a streamed CSV of all data, optionally filtered.'

    def generate():
        'A generator is required to stream the actual CSV.'
        fake_file = StringIO()
        w = csv.writer(fake_file)
        w.writerow(('URL', 'Status', 'Content-Type', 'Updated'))
        (yield fake_file.getvalue())
        fake_file.seek(0)
        fake_file.truncate(0)
        for (url_hash, data) in urls:
            data = apply_filters(data, filters, excludes)
            if (not data):
                continue
            status = data.get('final-status-code', '')
            if (not status):
                continue
            url = data['checked-url']
            content_type = data.get('content-type', '')
            updated = data.get('updated', '')
            w.writerow((url, status, content_type, updated))
            (yield fake_file.getvalue())
            fake_file.seek(0)
            fake_file.truncate(0)
    headers = Headers()
    headers.set('Content-Disposition', 'attachment', filename='croquemort-{date_iso}.csv'.format(date_iso=datetime.now().date().isoformat()))
    return Response(generate(), mimetype='text/csv', headers=headers)

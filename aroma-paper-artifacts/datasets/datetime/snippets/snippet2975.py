from datetime import datetime
import redis
from nameko.extensions import DependencyProvider
from kombu.utils.encoding import str_to_bytes
from .tools import generate_hash_for


def store_metadata(self, url, response):
    url_hash = generate_hash_for('url', url)
    self.database.hset(url_hash, 'final-url', str_to_bytes(response.url))
    self.database.hset(url_hash, 'final-status-code', str_to_bytes(response.status_code))
    self.database.hset(url_hash, 'updated', str_to_bytes(datetime.now().isoformat()))
    if response.headers:
        for header in HEADERS:
            value = response.headers.get(header, '')
            if ((header == 'content-type') and (';' in value)):
                self.store_content_type(url_hash, value)
            else:
                self.database.hset(url_hash, header, str_to_bytes(value))
    if len(response.history):
        self.database.hset(url_hash, 'redirect-url', str_to_bytes(response.history[0].url))
        self.database.hset(url_hash, 'redirect-status-code', str_to_bytes(response.history[0].status_code))
    return self.get_url(url_hash)

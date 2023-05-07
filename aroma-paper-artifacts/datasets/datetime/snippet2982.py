from datetime import datetime
import redis
from nameko.extensions import DependencyProvider
from kombu.utils.encoding import str_to_bytes
from .tools import generate_hash_for


def set_cache(self, key, content):
    self.database.hset(key, 'timestamp', str_to_bytes(datetime.now().isoformat()))
    self.database.hset(key, 'content', str_to_bytes(content))

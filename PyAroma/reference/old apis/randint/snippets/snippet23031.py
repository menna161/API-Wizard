import datetime
import random
import time
import unittest
import uuid
from pamqp import body, commands, constants, header
from aiorabbit import message


def setUp(self) -> None:
    self.exchange = str(uuid.uuid4())
    self.routing_key = str(uuid.uuid4())
    self.app_id = str(uuid.uuid4())
    self.content_encoding = str(uuid.uuid4())
    self.content_type = str(uuid.uuid4())
    self.correlation_id = str(uuid.uuid4())
    self.delivery_mode = random.randint(1, 2)
    self.expiration = str((int(time.time()) + random.randint(60, 300)))
    self.headers = {str(uuid.uuid4()): str(uuid.uuid4())}
    self.message_id = str(uuid.uuid4())
    self.message_type = str(uuid.uuid4())
    self.priority = random.randint(0, 255)
    self.reply_to = str(uuid.uuid4())
    self.timestamp = datetime.datetime.now()
    self.user_id = str(uuid.uuid4())
    self.body = b'-'.join([str(uuid.uuid4()).encode('latin-1') for _offset in range(0, random.randint(1, 100))])
    self.message = message.Message(self.get_method())
    self.message.header = header.ContentHeader(0, len(self.body), commands.Basic.Properties(app_id=self.app_id, content_encoding=self.content_encoding, content_type=self.content_type, correlation_id=self.correlation_id, delivery_mode=self.delivery_mode, expiration=self.expiration, headers=self.headers, message_id=self.message_id, message_type=self.message_type, priority=self.priority, reply_to=self.reply_to, timestamp=self.timestamp, user_id=self.user_id))
    value = bytes(self.body)
    while value:
        self.message.body_frames.append(body.ContentBody(value[:constants.FRAME_MAX_SIZE]))
        value = value[constants.FRAME_MAX_SIZE:]

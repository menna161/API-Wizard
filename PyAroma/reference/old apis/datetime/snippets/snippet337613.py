from datetime import datetime, date
from enum import Enum
from flask import Flask, url_for
from flask_babel import _
from money import Money
from passlib.hash import pbkdf2_sha256
from appkernel import AuditableRepository, MongoRepository, AppKernelException, ValidationException, Email, Unique
from appkernel import IdentityMixin, Role, CurrentSubject, Anonymous, TextIndex, Index
from appkernel import Max, Min
from appkernel import Model, Property, UniqueIndex
from appkernel import NotEmpty, Regexp, Past, Future, create_uuid_generator, date_now_generator, content_hasher
from appkernel import ServiceException
from appkernel.generators import TimestampMarshaller, MongoDateTimeMarshaller
from appkernel.model import action, resource
import urllib


def complete(self):
    self.completed = True
    self.closed_date = datetime.now()

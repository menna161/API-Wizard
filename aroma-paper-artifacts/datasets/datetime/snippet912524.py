from hashlib import sha1
import datetime
from django.contrib.auth.models import User
from django.core import mail
from django.core.mail import EmailMessage
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings


@property
def date_passed(self):
    return (datetime.date.today() > (self.date + datetime.timedelta(days=14)))

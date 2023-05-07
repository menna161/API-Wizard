from datetime import datetime
from dexy.filters.api import ApiFilter
import dexy.exceptions
import getpass
import os
import urllib
import boto
from boto.s3.key import Key


def bucket_name(self):
    "\n        Figure out which S3 bucket name to use and create the bucket if it doesn't exist.\n        "
    bucket_name = self.read_param('AWS_BUCKET_NAME')
    if (not bucket_name):
        try:
            username = getpass.getuser()
            bucket_name = ('dexy-%s' % username)
            return bucket_name
        except dexy.exceptions.UserFeedback:
            print("Can't automatically determine username. Please specify AWS_BUCKET_NAME for upload to S3.")
            raise
    bucket_name = datetime.now().strftime(bucket_name)
    self.log_debug(('S3 bucket name is %s' % bucket_name))
    return bucket_name

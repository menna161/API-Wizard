import boto3
import cfnresponse
import time
import traceback
from datetime import datetime


def wait_for_ses_domain_verification(self):
    start = datetime.now()
    status = 'Failed'
    while ((datetime.now() - start).total_seconds() < 240):
        result = self.ses.get_identity_verification_attributes(Identities=[self.domain])['VerificationAttributes']
        if (self.domain in result):
            status = result[self.domain]['VerificationStatus']
            print(('Status: ' + status))
            if (status == 'Success'):
                break
            time.sleep(5)
    if (status != 'Success'):
        raise Exception('Verification took to long. Aborting...')

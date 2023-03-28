import datetime
import jwt
from appkernel.configuration import config


@property
def auth_token(self):
    if (not self.id):
        raise AttributeError('The id of the Identity is not defined.')
    payload = {'exp': (datetime.datetime.utcnow() + datetime.timedelta(seconds=IdentityMixin.token_validity_in_seconds)), 'iat': datetime.datetime.utcnow(), 'sub': self.id}
    if (self.roles and isinstance(self.roles, list) and (len(self.roles) > 0)):
        payload.update(roles=self.roles)
    return jwt.encode(payload, key=config.private_key, algorithm='RS256').decode('utf-8')

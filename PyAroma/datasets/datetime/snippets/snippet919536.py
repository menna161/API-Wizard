from datetime import datetime
import pytest
from starlette_auth.tokens import token_generator
from starlette_auth.utils.http import urlsafe_base64_encode


def test_get_user_url_is_invalid_by_logging_in(client, user):
    uidb64 = urlsafe_base64_encode(bytes(str(user.id), encoding='utf-8'))
    token = token_generator.make_token(user)
    url = client.app.url_path_for('auth:password_reset_confirm', uidb64=uidb64, token=token)
    user.last_login = datetime.utcnow()
    user.save()
    response = client.get(url)
    assert (response.status_code == 404)

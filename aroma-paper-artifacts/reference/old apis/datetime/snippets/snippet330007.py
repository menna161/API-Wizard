from datetime import datetime, timedelta
from http.cookies import SimpleCookie
from sanic import Sanic
from sanic.response import json, text
from sanic.utils import sanic_endpoint_test


def test_cookie_options():
    app = Sanic('test_text')

    @app.route('/')
    def handler(request):
        response = text('OK')
        response.cookies['test'] = 'at you'
        response.cookies['test']['httponly'] = True
        response.cookies['test']['expires'] = (datetime.now() + timedelta(seconds=10))
        return response
    (request, response) = sanic_endpoint_test(app)
    response_cookies = SimpleCookie()
    response_cookies.load(response.headers.get('Set-Cookie', {}))
    assert (response_cookies['test'].value == 'at you')
    assert (response_cookies['test']['httponly'] == True)

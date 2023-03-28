from datetime import datetime
from django.shortcuts import redirect, render
from django.views.generic import ListView
from hello.forms import LogMessageForm
from hello.models import LogMessage


def hello_there(request, name):
    'Renders the hello_there page.\n    Args:\n        name: Name to say hello to\n    '
    return render(request, 'hello/hello_there.html', {'name': name, 'date': datetime.now()})

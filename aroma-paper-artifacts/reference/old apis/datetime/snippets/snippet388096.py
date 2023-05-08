from datetime import datetime
from django.shortcuts import redirect, render
from django.views.generic import ListView
from hello.forms import LogMessageForm
from hello.models import LogMessage


def log_message(request):
    form = LogMessageForm((request.POST or None))
    if (request.method == 'POST'):
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect('home')
        else:
            return render(request, 'hello/log_message.html', {'form': form})
    else:
        return render(request, 'hello/log_message.html', {'form': form})

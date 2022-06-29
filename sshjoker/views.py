from django.http import HttpResponseRedirect
from django.shortcuts import render

from users.models import UserStatus


def error_handler(request):
    return render(request, '403.html')


handler403 = error_handler
handler404 = error_handler


def home(request):
    if request.user.is_authenticated:
        if request.user.userdetail.status == UserStatus.INACTIVE:
            return HttpResponseRedirect('registration')
        if request.user.userdetail.status == UserStatus.REQUEST:
            return HttpResponseRedirect('accept-status')
    return render(request, 'home.html')
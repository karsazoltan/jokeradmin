from django.shortcuts import render


def error_handler(request):
    return render(request, '403.html')


handler403 = error_handler
handler404 = error_handler

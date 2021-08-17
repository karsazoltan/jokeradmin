from django.shortcuts import render

# Create your views here.
from users.models import UserDetail


def userpage(request):
    userdetail = UserDetail.objects.filter(user=request.user).get()
    return render(request, 'users/user.html', { 'userdetail': userdetail })
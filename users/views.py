from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from users.forms import SystemUserForm
from users.models import UserDetail, SystemUser


@login_required
def userpage(request):
    try:
        userdetail = UserDetail.objects.filter(user=request.user).get()
    except ObjectDoesNotExist:
        raise Http404('Adatok nem találhatóak')
    return render(request, 'users/user.html', { 'userdetail': userdetail })


def registration(request):

    return render(request, 'users/registration.html')

@login_required
def edituser(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied
    user = get_user_model().objects.get(pk=id)
    systemusers = SystemUser.objects.all()
    return render(request, 'users/edituser.html', { 'user': user, 'systemusers':systemusers })

@login_required
def systemuser(request):
    cmd = ''
    if request.GET.get('cmd'):
        cmd = request.GET.get('cmd')
    if request.method == 'POST':
        form = SystemUserForm(request.POST)
        if form.is_valid():
            cmd = form.newSystemUser()
            return HttpResponseRedirect(f'/systemuser?cmd={cmd}')
    else:
        form = SystemUserForm()

    systemusers = SystemUser.objects.all()
    return render(request, 'users/systemuser.html', { 'form': form, 'cmd': cmd, 'systemusers': systemusers})

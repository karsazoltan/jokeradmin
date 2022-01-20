from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from jokerauth.models import SSHKey
from jokerauth.service import savekeys
from users.forms import SystemUserForm, RegistrationForm, SetSysUserForm
from users.models import UserDetail, SystemUser


@login_required
def userpage(request):
    try:
        userdetail = UserDetail.objects.filter(user=request.user).get()
    except ObjectDoesNotExist:
        raise Http404('Adatok nem találhatóak')
    return render(request, 'users/user.html', {'userdetail': userdetail})


def registration(request):
    regok = False
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.createUser()
            regok = True
            return render(request, 'users/registration.html', {'regok': regok, 'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'users/registration.html', {'regok': regok, 'form': form})


@login_required
def edituser(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied
    user = get_user_model().objects.get(pk=id)
    systemusers = SystemUser.objects.all().filter(project__isnull=True)
    prevpage = '/users'
    if request.GET.get('prev'):
        prevpage = request.GET.get('prev')
    if request.method == 'POST':
        form = SetSysUserForm(request.POST, user=user)
        if form.is_valid():
            form.setSysUser()
            return HttpResponseRedirect(f'/edituser/{id}?prev={prevpage}')
    else:
        form = SetSysUserForm()
    return render(request, 'users/edituser.html', {'userinfo': user, 'systemusers': systemusers, 'form': form,
                                                   'prevpage': prevpage})


@login_required
def activateuser(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied
    user = get_user_model().objects.get(pk=id)
    user.is_active = True
    user.save()
    return HttpResponseRedirect(f'/edituser/{id}')


@login_required
def delete_sysuser_from_user(request, webuser_id, sysuser_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    try:
        webuser = User.objects.get(pk=webuser_id)
        sysuser = SystemUser.objects.get(pk=sysuser_id)
    except ObjectDoesNotExist:
        raise Http404('Objektum nem található')
    webuser.userdetail.systemuser.remove(sysuser)
    keys = SSHKey.objects.filter(user__userdetail__systemuser__exact=sysuser).filter(active=True)
    savekeys(keys, sysuser)
    return HttpResponseRedirect('/edituser/' + str(webuser_id))


@login_required
def users(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    pagination = False
    userfilter = ''
    if request.GET.get('search'):
        pagination = True
        userfilter = request.GET.get('search')
    all_users = get_user_model().objects.filter(is_active=True).filter(username__contains=userfilter).order_by(
        '-username')
    paginator = Paginator(all_users, 6)
    page_number = 1
    if request.GET.get('page'):
        pagination = True
        page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    return render(request, 'users/users.html',
                  {'users': users, 'page': page_number, 'maxpage': paginator.num_pages, 'filter': userfilter,
                   'pagination': pagination})


@login_required
def systemuser(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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
    return render(request, 'users/systemuser.html', {'form': form, 'cmd': cmd, 'systemusers': systemusers})


@login_required
def inactiveusers(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    users = User.objects.filter(is_active=False)
    return render(request, 'users/inactiveusers.html', {'users': users})

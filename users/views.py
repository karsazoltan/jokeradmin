import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from jokerauth.models import SSHKey
from jokerauth.service import save_keys
from sshjoker.settings import FROM_EMAIL, EMAIL_FOOTER
from users.forms import SystemUserForm, RegistrationForm, SetSysUserForm, BroadcastMailForm
from users.models import UserDetail, SystemUser, UserStatus


@login_required
def userpage(request):
    if request.user.userdetail.status == UserStatus.INACTIVE:
        return HttpResponseRedirect('registration')
    if request.user.userdetail.status == UserStatus.REQUEST:
        return HttpResponseRedirect('accept-status')
    try:
        userdetail = UserDetail.objects.filter(user=request.user).get()
    except ObjectDoesNotExist:
        raise Http404('Adatok nem találhatóak')
    return render(request, 'users/user.html', {'userdetail': userdetail})


@login_required
def registration(request):
    if request.user.userdetail.status == UserStatus.OK:
        return HttpResponseRedirect('')
    regok = request.user.userdetail.status == UserStatus.REQUEST
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.createUser(request.user)
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
    systemusers = user.userdetail.systemuser
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
    userdetail = user.userdetail
    userdetail.status = UserStatus.OK
    userdetail.save()
    send_mail('Kérelem elfogadva', f'Kérelmét elfogadták a következő felhasználóhoz: {user.username}' + EMAIL_FOOTER,
              FROM_EMAIL, [user.email])
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
    # keys = SSHKey.objects.filter(user__userdetail__systemuser__exact=sysuser).filter(active=True)
    save_keys.delay(sysuser.username, True)
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
    all_users = get_user_model().objects.filter(userdetail__status__exact=UserStatus.OK).filter(is_active=True) \
        .filter(username__contains=userfilter).order_by(
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
    users = User.objects.filter(userdetail__status__exact=UserStatus.REQUEST).filter(is_active=True)
    return render(request, 'users/inactiveusers.html', {'users': users})


@login_required
def mail_to_users(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    sent = ''
    if request.GET.get('sent'):
        sent = request.GET.get('sent')
    if request.method == 'POST':
        form = BroadcastMailForm(request.POST, user=request.user.username)
        if form.is_valid():
            try:
                form.sendmail()
            except:
                return HttpResponseRedirect(f'/mailview?sent=false')
            return HttpResponseRedirect(f'/mailview?sent=true')
    else:
        form = BroadcastMailForm()
    return render(request, 'mail/adminmail.html', {'form': form, 'sent': sent})


@login_required
def accept_status(request):
    if request.user.userdetail.status == UserStatus.OK:
        return HttpResponseRedirect('')
    return render(request, 'users/accept.html')


@login_required
def userdata(request):
    user = request.user
    return HttpResponse(
        json.dumps({
            'webuser': user.username,
            'username': user.userdetail.preferred.username
        }),
        content_type='application/json'
    )


def set_preferred_user(request, sysuser_id):
    systemusers = request.user.userdetail.systemuser.all()
    picksysuser = SystemUser.objects.get(pk=sysuser_id)
    if picksysuser not in systemusers:
        raise PermissionError()
    userdetail = request.user.userdetail
    userdetail.preferred = picksysuser
    userdetail.save()
    return HttpResponseRedirect('http://127.0.0.1:8010/hub/oauth_login?&next=')


@login_required
def jupyterhub(request):
    systemusers = request.user.userdetail.systemuser.all
    preferred = request.user.userdetail.preferred
    return render(request, 'users/jupyterhub.html', {'systemusers': systemusers, 'preferred': preferred})

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from jokerauth.forms import SSHKeyForm, AdminSSHKeyForm
from jokerauth.models import SSHKey
from sshjoker.settings import MAXKEYNUM


@login_required
def sshkey(request):
    keys = SSHKey.objects.filter(user=request.user)
    if request.method == 'POST':
        form = SSHKeyForm(request.POST, request=request)
        if form.is_valid():
            form.newKey(request.user)
            return HttpResponseRedirect('/sshkeys#form')
    else:
        form = SSHKeyForm(request=request)
    return render(request, 'jokerauth/sshkeys.html', {'form': form, 'keys': keys, 'maxkeynum': MAXKEYNUM})


@login_required
def adminkeys(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    userfilter = ''
    if request.GET.get('search'):
        userfilter = request.GET.get('search')
    allkeys = SSHKey.objects.filter(user__username__contains=userfilter).order_by('-create_date')
    users = get_user_model().objects.all()
    paginator = Paginator(allkeys, 5)
    page_number = 1
    if request.GET.get('page'):
        page_number = request.GET.get('page')
    keys = paginator.get_page(page_number)

    if request.method == 'POST':
        form = AdminSSHKeyForm(request.POST)
        if form.is_valid():
            form.newKey()
            return HttpResponseRedirect('admin')
    else:
        form = AdminSSHKeyForm()
    return render(request, 'jokerauth/adminkeys.html',
                  {'allkeys': keys, 'form': form, 'users': users,
                   'page': page_number, 'maxpage': paginator.num_pages, 'filter': userfilter})


@login_required
def activatekey(request, id):
    try:
        key = SSHKey.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise Http404('Kulcs nem található')
    if key.user == request.user:
        key.addtoserver()
    else:
        raise PermissionDenied
    return HttpResponseRedirect('/sshkeys')


@login_required
def adminactivate(request, id):
    try:
        key = SSHKey.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise Http404('Kulcs nem található')
    if request.user.is_superuser:
        key.addtoserver()
    else:
        raise PermissionDenied
    return HttpResponseRedirect('/sshkeys/admin')


@login_required
def deletekey(request, id):
    try:
        key = SSHKey.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise Http404('Kulcs nem található')
    if key.user == request.user:
        key.deleteit()
    else:
        raise PermissionDenied
    return HttpResponseRedirect('/sshkeys')


@login_required
def admindelete(request, id):
    try:
        key = SSHKey.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise Http404('Kulcs nem található')
    if request.user.is_superuser:
        key.deleteit()
    else:
        raise PermissionDenied
    return HttpResponseRedirect('/sshkeys/admin')
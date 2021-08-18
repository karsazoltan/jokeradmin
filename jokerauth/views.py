from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound, Http404, HttpResponse
from django.shortcuts import render
from jokerauth.forms import SSHKeyForm, AdminSSHKeyForm
from jokerauth.models import SSHKey


@login_required
def sshkey(request):
    keys = SSHKey.objects.filter(user=request.user)
    if request.method == 'POST':
        form = SSHKeyForm(request.POST)
        if form.is_valid():
            form.newKey(request.user)
            return HttpResponseRedirect('/sshkeys')
    else:
        form = SSHKeyForm()
    return render(request, 'jokerauth/sshkeys.html', {'form': form, 'keys': keys})

@login_required
def adminkeys(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    allkeys = SSHKey.objects.all()
    users = get_user_model().objects.all()
    if request.method == 'POST':
        form = AdminSSHKeyForm(request.POST)
        if form.is_valid():
            form.newKey()
            return HttpResponseRedirect('admin')
    else:
        form = AdminSSHKeyForm()
    return render(request, 'jokerauth/adminkeys.html', { 'allkeys': allkeys, 'form' : form, 'users': users })


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
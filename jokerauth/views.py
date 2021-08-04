from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from jokerauth.forms import SSHKeyForm
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
def activatekey(request, id):
    key = SSHKey.objects.get(pk=id)
    if key.user == request.user:
        key.addtoserver()
    return HttpResponseRedirect('/sshkeys')


@login_required
def deletekey(request, id):
    key = SSHKey.objects.get(pk=id)
    if key.user == request.user:
        key.delete()
    return HttpResponseRedirect('/sshkeys')
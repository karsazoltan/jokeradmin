from django import forms
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from jokerauth.models import SSHKey
from jokerauth.service import savekeys
from users.models import SystemUser, UserDetail
from users.service import adduser


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    neptun = forms.CharField(max_length=6)

    def clean(self):
        user = get_user_model().objects.filter(username=self.cleaned_data['username'])
        if user.count() == 1:
            raise ValidationError("Már van ilyen felhasználó: " + self.cleaned_data['username'])
        userdetail = UserDetail.objects.filter(neptun=self.cleaned_data['username'])
        if userdetail.count() == 1:
            raise ValidationError("Már van ilyen NEPTUN kód: " + self.cleaned_data['neptun'])


    def createUser(self):
        user = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'], self.cleaned_data['password'])
        user.is_active = False
        user.save()
        userdetail = UserDetail(user=user, neptun=self.cleaned_data['neptun'])
        userdetail.save()

class SystemUserForm(forms.Form):
    username = forms.RegexField(max_length=40, regex=r'[a-zA-Z0-9]+', error_messages={ 'invalid': ("Csak betűket és számokat tartalmazhat, maximum 40 karakter")} )

    def clean(self):
        user = SystemUser.objects.filter(username=self.cleaned_data['username'])
        if user.count() == 1:
            raise ValidationError("Már van ilyen: " + self.cleaned_data['username'])

    def newSystemUser(self):
        newSystemUser = SystemUser(username=self.cleaned_data['username'])
        newSystemUser.save()
        adduser(self.cleaned_data['username'])
        return newSystemUser.bashcmd()


class SetSysUserForm(forms.Form):
    systemuser = forms.CharField(max_length=40)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SetSysUserForm, self).__init__(*args, **kwargs)

    def clean(self):
        sysuser = SystemUser.objects.filter(username=self.cleaned_data['systemuser'])
        if sysuser.count() != 1:
            raise ValidationError("Nincs ilyen rendszer felhasználó!")

    def setSysUser(self):
        sysuser = SystemUser.objects.filter(username=self.cleaned_data['systemuser']).get()
        self.user.userdetail.systemuser.add(sysuser)
        self.user.userdetail.save()
        keys = SSHKey.objects.filter(user__userdetail__systemuser__exact=sysuser).filter(active=True)
        savekeys(keys, sysuser)

from django import forms
from django.core.exceptions import ValidationError

from users.models import SystemUser


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.PasswordInput()


class SystemUserForm(forms.Form):
    username = forms.RegexField(max_length=40, regex=r'[a-zA-Z0-9]+', error_messages={ 'invalid': ("Csak betűket és számokat tartalmazhat, maximum 40 karakter")} )

    def clean(self):
        user = SystemUser.objects.filter(username=self.cleaned_data['username'])
        if user.count() == 1:
            raise ValidationError("Már van ilyen: " + self.cleaned_data['username'])

    def newSystemUser(self):
        newSystemUser = SystemUser(username=self.cleaned_data['username'])
        newSystemUser.save()
        return newSystemUser.bashcmd()


class SetSysUserForm(forms.Form):
    systemuser = forms.CharField(max_length=40)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SetSysUserForm, self).__init__(*args, **kwargs)

    def clean(self):
        user = SystemUser.objects.filter(username=self.cleaned_data['username'])
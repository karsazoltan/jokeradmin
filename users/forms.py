from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from jokerauth.service import save_keys
from sshjoker.settings import FROM_EMAIL, EMAIL_FOOTER
from users.models import SystemUser, UserDetail, UserStatus
from users.service import adduser


class RegistrationForm(forms.Form):
    description = forms.CharField(max_length=500)

    def clean(self):
        if len(self.cleaned_data['description']) < 30:
            raise ValidationError("Írjon legalább 30 karakter hosszúságú leírást!")

    def createUser(self, user):
        user_detail = user.userdetail
        user_detail.status = UserStatus.REQUEST
        user_detail.description = self.cleaned_data['description']
        self.sendmail(user.username, user.email, user.last_name + user.first_name, user.userdetail.description)
        user_detail.save()

    def sendmail(self, username, email, name, desc):
        users = User.objects.filter(is_superuser=True).all()
        mails = map(lambda u: u.email, users)
        send_mail("Új kérelem - Joker", f"Új felhasználó regisztrált a következő adatokkal: \n {username} - {name} \n {email} \n Kérelem törzse: {desc}" + EMAIL_FOOTER, FROM_EMAIL, mails)


class SystemUserForm(forms.Form):
    username = forms.RegexField(max_length=40, regex=r'[a-zA-Z0-9]+',
                                error_messages={'invalid':
                                                    "Csak betűket és számokat tartalmazhat, maximum 40 karakter"})

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        if username:
            user = SystemUser.objects.filter(username=username)
            if user.count() == 1:
                raise ValidationError("Már van ilyen: " + self.cleaned_data['username'])

    def newSystemUser(self):
        newSystemUser = SystemUser(username=self.cleaned_data['username'])
        newSystemUser.save()
        adduser.delay(self.cleaned_data['username'])
        return newSystemUser.bashcmd()


class SetSysUserForm(forms.Form):
    systemuser = forms.CharField(max_length=40)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SetSysUserForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.cleaned_data.get('systemuser'):
            sysuser = SystemUser.objects.filter(username=self.cleaned_data['systemuser']).filter(project__isnull=True)
            if sysuser.count() != 1:
                raise ValidationError(
                    "Nincs ilyen rendszer felhasználó! Lehet egy projekthez társított felhasználóval próbálkozott!")
        else:
            raise ValidationError("Üres rendszernév")

    def setSysUser(self):
        sysuser = SystemUser.objects.filter(username=self.cleaned_data['systemuser']).get()
        self.user.userdetail.systemuser.add(sysuser)
        self.user.userdetail.save()
        # keys = SSHKey.objects.filter(user__userdetail__systemuser__exact=sysuser).filter(active=True)
        save_keys.delay(sysuser.username, True)


class BroadcastMailForm(forms.Form):
    subject = forms.CharField(max_length=40)
    body = forms.CharField(max_length=300)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BroadcastMailForm, self).__init__(*args, **kwargs)

    def sendmail(self):
        users = User.objects.filter(is_active=True).filter(userdetail__status__exact='OK').all()
        mails = map(lambda u: u.email, users)
        send_mail(self.cleaned_data['subject'] + ' (' + self.user + ')', self.cleaned_data['body'] + EMAIL_FOOTER, FROM_EMAIL, mails)
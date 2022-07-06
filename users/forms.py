from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from jokerauth.service import save_keys
from sshjoker.settings import FROM_EMAIL, EMAIL_FOOTER
from users.models import SystemUser, UserStatus
from users.service import adduser
from django.utils.translation import gettext as _


class RegistrationForm(forms.Form):
    description = forms.CharField(max_length=500)

    def clean(self):
        if len(self.cleaned_data['description']) < 50:
            raise ValidationError(_('Description must be at least 50 characters long (max 500)'))

    def createUser(self, user):
        user_detail = user.userdetail
        user_detail.status = UserStatus.REQUEST
        user_detail.description = self.cleaned_data['description']
        self.sendmail(user.username, user.email, user.last_name + ' ' + user.first_name, user.userdetail.description)
        user_detail.save()

    def sendmail(self, username, email, name, desc):
        users = User.objects.filter(is_superuser=True).all()
        mails = map(lambda u: u.email, users)
        send_mail("New request - Joker",
                  f"New request for Joker, user data: \n {username} - {name} \n {email} \n Request body: {desc}"
                  + EMAIL_FOOTER, FROM_EMAIL, mails)


class SystemUserForm(forms.Form):
    username = forms.RegexField(max_length=40, regex=r'[a-zA-Z0-9]+',
                                error_messages={'invalid': "It can only contain letters and numbers, max 40 character"})

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        if username:
            user = SystemUser.objects.filter(username=username)
            if user.count() == 1:
                raise ValidationError(_('Already exists ') + self.cleaned_data['username'])

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
                    _('There is no such linux user! Maybe you tried with a user associated with a project!'))
        else:
            raise ValidationError(_('Systemuser is empty'))

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
        send_mail(self.cleaned_data['subject'] + ' (' + self.user + ')', self.cleaned_data['body'] + EMAIL_FOOTER,
                  FROM_EMAIL, mails)

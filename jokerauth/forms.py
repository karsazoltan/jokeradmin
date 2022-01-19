from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from jokerauth.models import SSHKey
from sshjoker.settings import MAXKEYNUM


class SSHKeyForm(forms.Form):
    comment = forms.CharField(max_length=100)
    pubkey = forms.CharField(widget=forms.Textarea, max_length=1000)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SSHKeyForm, self).__init__(*args, **kwargs)

    def clean(self):
        if not self.cleaned_data.get('comment') or not self.cleaned_data.get('pubkey'):
            raise ValidationError("Töltse ki az összes mezőt!")
        userKeyNum = SSHKey.objects.filter(user=self.request.user).count()
        if MAXKEYNUM < userKeyNum + 1:
            raise ValidationError("Maximális kulcsszám elérve!")
        try:
            systemuser = self.request.user.userdetail.systemuser
        except:
            raise ValidationError("A fiókhoz még nem tartozik társított rendszerfelhasználó (linux user). Kérje meg az egyik admin felhasználót, hogy állítsa be. ")
        if self.cleaned_data['pubkey'].count('ssh-rsa') != 1:
            raise ValidationError("Vagy több kulcs található benne, vagy nem tartalmaz érvényes ssh-rsa kulcsot.")

    def newKey(self, user):
        newkey = SSHKey(user=user, active=False, comment=self.cleaned_data['comment'], pubkey=self.cleaned_data['pubkey'])
        newkey.save()


class AdminSSHKeyForm(forms.Form):
    username = forms.CharField(max_length=100)
    comment = forms.CharField(max_length=100)
    pubkey = forms.CharField(widget=forms.Textarea, max_length=1000)

    def clean(self):
        if not self.cleaned_data.get('username') or not self.cleaned_data.get('comment') or not self.cleaned_data.get('pubkey'):
            raise ValidationError("Töltse ki az összes mezőt!")
        user = get_user_model().objects.filter(username=self.cleaned_data['username'])
        if user.count() != 1:
            raise ValidationError("Nincs ilyen felhasználó: " + self.cleaned_data['username'])
        return self.cleaned_data

    def newKey(self):
        user = get_user_model().objects.filter(username=self.cleaned_data['username']).get()
        newkey = SSHKey(user=user, active=False, comment=self.cleaned_data['comment'], pubkey=self.cleaned_data['pubkey'])
        newkey.save()
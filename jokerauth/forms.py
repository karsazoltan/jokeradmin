from django import forms

from jokerauth.models import SSHKey


class SSHKeyForm(forms.Form):
    comment = forms.CharField(max_length=100)
    pubkey = forms.CharField(widget=forms.Textarea, max_length=1000)

    def newKey(self, user):
        newkey = SSHKey(user=user, active=False, comment=self.cleaned_data['comment'], pubkey=self.cleaned_data['pubkey'])
        newkey.save()
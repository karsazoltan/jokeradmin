from django import forms
from django.core.exceptions import ValidationError

from jokerauth.models import SSHKey
from jokerauth.service import savekeys
from projects.models import Project
from django.contrib.auth import get_user_model

from users.models import SystemUser
from users.service import adduser


class AdminProjectForm(forms.Form):
    title = forms.CharField(max_length=100)
    owner = forms.CharField(max_length=100)
    system_user = forms.RegexField(max_length=40, regex=r'[a-zA-Z0-9]+', error_messages={ 'invalid': ("Csak betűket és számokat tartalmazhat, maximum 40 karakter")} )
    partners = forms.CharField(max_length=200, empty_value="", required=False)
    description = forms.CharField(widget=forms.Textarea, max_length=1000)
    public = forms.BooleanField(required=False, initial=False)

    def clean(self):
        super().clean()
        if self.cleaned_data.get('owner'):
            owner = get_user_model().objects.filter(username__icontains=self.cleaned_data['owner'])
            if owner.count() == 0:
                raise ValidationError("Nincs ilyen felhasználó tulajdonosnak: " + self.cleaned_data['owner'])
            elif owner.count() > 1:
                raise ValidationError("Több felhasználó neve is illeszkedik: " + self.cleaned_data['owner'])

        if self.cleaned_data.get('partners'):
            partnersusername = self.cleaned_data['partners'].split(',')
            for partnername in partnersusername:
                if partnername != "":
                    partner = get_user_model().objects.filter(username__icontains=partnername.strip())
                    if partner.count() != 1:
                        raise ValidationError("Nincs ilyen felhasználó partnernek: " + partnername)
                    elif partner.count() > 1:
                        raise ValidationError("Több felhasználó neve is illeszkedik: " + partnername)
                    if partner.get() == owner.get():
                        raise ValidationError("Partner és tulajdonos nem lehet egyszerre: " + partnername)

        return self.cleaned_data

    def newProject(self):
        user = SystemUser.objects.filter(username=self.cleaned_data['system_user'])
        if user.count() == 0:
            newSystemUser = SystemUser(username=self.cleaned_data['system_user'])
            newSystemUser.save()
            adduser(self.cleaned_data['system_user'])

        system_user = SystemUser.objects.filter(username=self.cleaned_data['system_user']).get()

        owner = get_user_model().objects.filter(username=self.cleaned_data['owner']).get()
        owner.userdetail.systemuser.add(system_user)
        owner.userdetail.save()

        newproject = Project(
            owner=owner,
            system_user=system_user,
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            public=self.cleaned_data['public'])
        newproject.save()

        if self.cleaned_data.get('partners'):
            partnersusername = self.cleaned_data['partners'].split(',')
            for partnername in partnersusername:
                if partnername != "":
                    partner = get_user_model().objects.filter(username=partnername.strip()).get()
                    newproject.users.add(partner)
                    partner.userdetail.systemuser.add(system_user)
                    partner.userdetail.save()

        newproject.save()

        keys = SSHKey.objects.filter(user__userdetail__systemuser__exact=system_user).filter(active=True)
        savekeys(keys, system_user)

class AddPartnerForm(forms.Form):
    user = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddPartnerForm, self).__init__(*args, **kwargs)

    def clean(self):
        user = get_user_model().objects.filter(username=self.cleaned_data['user'])
        if user.count() == 0:
            raise ValidationError("Nincs ilyen felhasználó: " + self.cleaned_data['user'])
        if user.get() == self.request.user:
            raise ValidationError("Már tulajdonos vagy!")
        return self.cleaned_data

    def addpartner(self, project):
        user = get_user_model().objects.filter(username=self.cleaned_data['user']).get()
        project.users.add(user)
        user.userdetail.systemuser.add(project.system_user)
        user.userdetail.save()
        keys = SSHKey.objects.filter(user__userdetail__systemuser__exact=project.system_user).filter(active=True)
        savekeys(keys, project.system_user)

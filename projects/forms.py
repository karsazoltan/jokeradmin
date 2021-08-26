from django import forms
from django.core.exceptions import ValidationError

from projects.models import Project
from django.contrib.auth import get_user_model


class ProjectForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea, max_length=1000)
    public = forms.BooleanField(required=False, initial=False)

    def newProject(self, user):
        newproject = Project(
            owner=user,
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            public=self.cleaned_data['public'])
        newproject.save()

class AdminProjectForm(forms.Form):
    title = forms.CharField(max_length=100)
    owner = forms.CharField(max_length=100)
    partners = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea, max_length=1000)
    public = forms.BooleanField(required=False, initial=False)

    def clean(self):
        owner = get_user_model().objects.filter(username__icontains=self.cleaned_data['owner'])
        if owner.count() == 0:
            raise ValidationError("Nincs ilyen felhasználó tulajdonosnak: " + self.cleaned_data['owner'])
        elif owner.count() > 1:
            raise ValidationError("Több felhasználó neve is illeszkedik: " + self.cleaned_data['owner'])
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
        owner = get_user_model().objects.filter(username__icontains=self.cleaned_data['owner']).get()
        newproject = Project(
            owner=owner,
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            public=self.cleaned_data['public'])
        newproject.save()
        partnersusername = self.cleaned_data['partners'].split(',')
        for partnername in partnersusername:
            if partnername != "":
                partner = get_user_model().objects.filter(username__icontains=partnername.strip()).get()
                newproject.users.add(partner)
        newproject.save()

class AddPartnerForm(forms.Form):
    user = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddPartnerForm, self).__init__(*args, **kwargs)

    def clean(self):
        user = get_user_model().objects.filter(username__icontains=self.cleaned_data['user'])
        if user.count() == 0:
            raise ValidationError("Nincs ilyen felhasználó: " + self.cleaned_data['user'])
        if user.get() == self.request.user:
            raise ValidationError("Már tulajdonos vagy!")
        return self.cleaned_data

    def addpartner(self, project):
        user = get_user_model().objects.filter(username__icontains=self.cleaned_data['user']).get()
        project.users.add(user)

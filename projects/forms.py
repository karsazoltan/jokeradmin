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


class AddPartnerForm(forms.Form):
    user = forms.CharField(max_length=200)

    def clean(self):
        user = get_user_model().objects.filter(username__icontains=self.cleaned_data['user'])
        if user.count() == 0:
            raise ValidationError("Nincs ilyen felhasználó")
        return self.cleaned_data

    def addpartner(self, project):
        user = get_user_model().objects.filter(username__icontains=self.cleaned_data['user']).get()
        project.users.add(user)

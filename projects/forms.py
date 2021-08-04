from django import forms
from projects.models import Project


class ProjectForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea, max_length=1000)
    public = forms.BooleanField()

    def newProject(self, user):
        newproject = Project(
            owner=user,
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            public=self.cleaned_data['public'])
        newproject.save()

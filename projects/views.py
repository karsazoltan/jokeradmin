from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from projects.forms import ProjectForm
from projects.models import Project


@login_required
def projects(request):
    projects = Project.objects.filter(owner=request.user)
    partnerprojects = request.user.project_set.all()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.newProject(request.user)
            return HttpResponseRedirect('/projects')
    else:
        form = ProjectForm()
    return render(request, 'projects/project.html',
                  {'form': form, 'projects': projects, 'partnerprojects': partnerprojects })

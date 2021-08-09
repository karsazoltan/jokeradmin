from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from projects.forms import ProjectForm
from projects.models import Project


@login_required
def projects(request):
    projects = Project.objects.filter(owner=request.user)
    partnerprojects = request.user.projects.all()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.newProject(request.user)
            return HttpResponseRedirect('/projects')
    else:
        form = ProjectForm()
    return render(request, 'projects/project.html',
                  {'form': form, 'projects': projects, 'partnerprojects': partnerprojects })

@login_required
def details(request, id):
    project = Project.objects.get(pk=id)
    return render(request, 'projects/details.html',
                  { 'project' : project })

@login_required
def deleteproject(request, id):
    project = Project.objects.get(pk=id)
    if request.user == project.owner:
        project.delete()
    else:
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/projects')
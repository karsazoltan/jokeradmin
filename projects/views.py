from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import get_user_model

from projects.forms import ProjectForm, AddPartnerForm
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
    partners = project.users.all()
    users = get_user_model().objects.all()
    if request.method == 'POST':
        form = AddPartnerForm(request.POST)
        if form.is_valid():
            form.addpartner(project)
            return HttpResponseRedirect('/projects/' + str(id))
    else:
        form = AddPartnerForm()
    return render(request, 'projects/details.html',
                  { 'project' : project, 'users': users, 'form': form, 'partners' : partners })

@login_required
def deletepartner(request, project_id, partner_id):
    project = Project.objects.get(pk=project_id)
    partner = get_user_model().objects.get(pk=partner_id)
    if request.user == project.owner:
        project.users.remove(partner)
    return HttpResponseRedirect('/projects/' + str(project_id))


@login_required
def deleteproject(request, id):
    project = Project.objects.get(pk=id)
    if request.user == project.owner:
        project.delete()
    else:
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/projects')
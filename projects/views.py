from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth import get_user_model

from projects.forms import ProjectForm, AddPartnerForm, AdminProjectForm
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
def adminprojects(request):
    projects = Project.objects.all()
    users = get_user_model().objects.all()
    if request.method == 'POST':
        form = AdminProjectForm(request.POST)
        if form.is_valid():
            form.newProject()
            return HttpResponseRedirect('/projects/admin')
    else:
        form = AdminProjectForm()
    return render(request, 'projects/adminproject.html',
                  {'form': form, 'projects': projects, 'users': users})


@login_required
def details(request, id):
    project = Project.objects.get(pk=id)
    partners = project.users.all()
    users = get_user_model().objects.all()
    if request.method == 'POST':
        form = AddPartnerForm(request.POST, request=request)
        if form.is_valid():
            form.addpartner(project)
            return HttpResponseRedirect('/projects/' + str(id))
    else:
        form = AddPartnerForm(request=request)
    return render(request, 'projects/details.html',
                  { 'project' : project, 'users': users, 'form': form, 'partners' : partners })

@login_required
def deletepartner(request, project_id, partner_id):
    try:
        project = Project.objects.get(pk=project_id)
        partner = get_user_model().objects.get(pk=partner_id)
    except ObjectDoesNotExist:
        raise Http404('Objektum nem található')
    if request.user == project.owner:
        project.users.remove(partner)
    else:
        raise PermissionDenied
    return HttpResponseRedirect('/projects/' + str(project_id))


@login_required
def deleteproject(request, id):
    try:
        project = Project.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise Http404('Projekt nem található')
    if request.user == project.owner:
        project.delete()
    else:
        raise PermissionDenied
    return HttpResponseRedirect('/projects')
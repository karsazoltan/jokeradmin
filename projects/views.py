from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth import get_user_model

from jokerauth.models import SSHKey
from jokerauth.service import save_keys
from projects.forms import AddPartnerForm, AdminProjectForm, EditDescription
from projects.models import Project
from users.models import UserStatus


@login_required
def projects(request):
    if request.user.userdetail.status == UserStatus.INACTIVE:
        return HttpResponseRedirect('registration')
    if request.user.userdetail.status == UserStatus.REQUEST:
        return HttpResponseRedirect('accept-status')
    projects = Project.objects.filter(owner=request.user)
    partnerprojects = request.user.projects.all()
    return render(request, 'projects/project.html',
                  {'projects': projects, 'partnerprojects': partnerprojects})


def public_projects(request):
    pagination = False
    userfilter = ''
    if request.GET.get('search'):
        pagination = True
        userfilter = request.GET.get('search')
    allprojects = Project.objects.filter(title__contains=userfilter).filter(public=True).order_by('-create_date')
    paginator = Paginator(allprojects, 5)
    page_number = 1
    if request.GET.get('page'):
        pagination = True
        page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    return render(request, 'projects/public.html',
                  { 'projects': projects,
                    'page': page_number, 'maxpage': paginator.num_pages, 'filter': userfilter, 'pagination': pagination })

@login_required
def adminprojects(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    pagination = False
    userfilter = ''
    if request.GET.get('search'):
        pagination = True
        userfilter = request.GET.get('search')
    allprojects = Project.objects.filter(owner__username__contains=userfilter).order_by('-create_date')
    users = get_user_model().objects.all()
    paginator = Paginator(allprojects, 5)
    page_number = 1
    if request.GET.get('page'):
        pagination = True
        page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)

    if request.method == 'POST':
        form = AdminProjectForm(request.POST)
        if form.is_valid():
            form.newProject()
            return HttpResponseRedirect('/projects/admin')
    else:
        form = AdminProjectForm()
    return render(request, 'projects/adminproject.html',
                  {'form': form, 'projects': projects, 'users': users,
                   'page': page_number, 'maxpage': paginator.num_pages, 'filter': userfilter, 'pagination': pagination})


@login_required
def details(request, id):
    if request.user.userdetail.status == UserStatus.INACTIVE:
        return HttpResponseRedirect('registration')
    if request.user.userdetail.status == UserStatus.REQUEST:
        return HttpResponseRedirect('accept-status')
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
                  {'project': project, 'users': users, 'form': form, 'partners': partners})


@login_required
def deletepartner(request, project_id, partner_id):
    if request.user.userdetail.status == UserStatus.INACTIVE:
        return HttpResponseRedirect('registration')
    if request.user.userdetail.status == UserStatus.REQUEST:
        return HttpResponseRedirect('accept-status')
    try:
        project = Project.objects.get(pk=project_id)
        partner = get_user_model().objects.get(pk=partner_id)
    except ObjectDoesNotExist:
        raise Http404()
    if request.user == project.owner or request.user.is_superuser:
        project.users.remove(partner)
        partner.userdetail.systemuser.remove(project.system_user)
        partner.userdetail.save()
        # keys = SSHKey.objects.filter(user__userdetail__systemuser__exact=project.system_user).filter(active=True)
        save_keys.delay(project.system_user.username, True)
    else:
        raise PermissionDenied
    return HttpResponseRedirect('/projects/' + str(project_id))


@login_required
def edit_description(request, id):
    if request.user.userdetail.status == UserStatus.INACTIVE:
        return HttpResponseRedirect('registration')
    if request.user.userdetail.status == UserStatus.REQUEST:
        return HttpResponseRedirect('accept-status')
    try:
        project = Project.objects.get(pk=id)
        if request.user == project.owner or request.user.is_superuser:
            if request.method == 'POST':
                form = EditDescription(request.POST)
                if form.is_valid():
                    form.edit_description(project)
            else:
                raise Http404()
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        raise Http404()
    return HttpResponseRedirect('/projects/' + str(id))


@login_required
def set_public(request, id):
    if request.user.userdetail.status == UserStatus.INACTIVE:
        return HttpResponseRedirect('registration')
    if request.user.userdetail.status == UserStatus.REQUEST:
        return HttpResponseRedirect('accept-status')
    try:
        project = Project.objects.get(pk=id)
        if request.user == project.owner or request.user.is_superuser:
            if project.public:
                project.public = False
            else:
                project.public = True
            project.save()
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        raise Http404()
    return HttpResponseRedirect('/projects/' + str(id))


@login_required
def deleteproject(request, id):
    if request.user.userdetail.status == UserStatus.INACTIVE:
        return HttpResponseRedirect('registration')
    if request.user.userdetail.status == UserStatus.REQUEST:
        return HttpResponseRedirect('accept-status')
    try:
        project = Project.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise Http404()
    if request.user == project.owner or request.user.is_superuser:
        for partner in project.users.all():
            partner.userdetail.systemuser.remove(project.system_user)
            partner.userdetail.save()
        # keys = SSHKey.objects.filter(user__userdetail__systemuser__exact=project.system_user).filter(active=True)
        save_keys.delay(project.system_user.username, True)
        project.delete()
    else:
        raise PermissionDenied
    return HttpResponseRedirect('/projects')

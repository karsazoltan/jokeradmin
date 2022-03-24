from django.urls import path, include
from rest_framework import routers

from . import views
from .restapi import ProjectViewSet

router = routers.DefaultRouter()
router.register(r'rest', ProjectViewSet)

urlpatterns = [
    path('project/', include(router.urls)),
    path('projects', views.projects, name='projects'),
    path('projects/public', views.public_projects, name='public_projects'),
    path('projects/admin', views.adminprojects, name='adminprojects'),
    path('projects/<int:id>/', views.details, name='details'),
    path('projects/<int:project_id>/deletepartner/<int:partner_id>/', views.deletepartner, name='deletepartner'),
    path('projects/delete/<int:id>/', views.deleteproject, name='deleteproject'),
    path('projects/public/<int:id>/', views.set_public, name='set_public'),
    path('projects/<int:id>/edit_desc', views.edit_description, name='edit_project_desc')
]
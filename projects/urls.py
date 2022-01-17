from django.urls import path
from . import views

urlpatterns = [
    path('projects', views.projects, name='projects'),
    path('projects/public', views.public_projects, name='public_projects'),
    path('projects/admin', views.adminprojects, name='adminprojects'),
    path('projects/<int:id>/', views.details, name='details'),
    path('projects/<int:project_id>/deletepartner/<int:partner_id>/', views.deletepartner, name='deletepartner'),
    path('projects/delete/<int:id>/', views.deleteproject, name='deleteproject'),
    path('projects/public/<int:id>/', views.set_public, name='set_public'),
    path('projects/<int:id>/edit_desc', views.edit_description, name='edit_project_desc')
]
from django.urls import path
from . import views

urlpatterns = [
    path('projects', views.projects, name='projects'),
    path('projects/admin', views.adminprojects, name='adminprojects'),
    path('projects/<int:id>/', views.details, name='details'),
    path('projects/<int:project_id>/deletepartner/<int:partner_id>/', views.deletepartner, name='deletepartner'),
    path('projects/delete/<int:id>/', views.deleteproject, name='deleteproject')
]
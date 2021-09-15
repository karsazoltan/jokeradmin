from django.urls import path
from . import views

urlpatterns = [
    path('user', views.userpage, name='user'),
    path('registration', views.registration, name='registration'),
    path('systemuser', views.systemuser, name='systemuser'),
    path('users', views.users, name='users'),
    path('inactiveusers', views.inactiveusers, name='inactiveusers'),
    path('edituser/<int:id>/', views.edituser, name='edituser'),
    path('activateuser/<int:id>/', views.activateuser, name='activateuser'),
    path('edituser/<int:webuser_id>/deletesysuser/<int:sysuser_id>/', views.delete_sysuser_from_user, name='delete_sys_from_webuser'),
]
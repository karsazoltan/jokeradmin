from django.urls import path, include
from rest_framework import routers

from users import restapi
from . import views

router = routers.DefaultRouter()
router.register(r'rest/webuser', restapi.UserViewSet)
router.register(r'rest/userdetail', restapi.UserDetailViewSet)
router.register(r'rest/sysuser', restapi.SystemUserViewSet)

urlpatterns = [
    path('user/', include(router.urls)),
    path('user', views.userpage, name='user'),
    path('registration', views.registration, name='registration'), # eduid-s azonosítás lesz
    path('accept-status', views.accept_status, name='accept-status'),
    path('systemuser', views.systemuser, name='systemuser'),
    path('users', views.users, name='users'),
    path('inactiveusers', views.inactiveusers, name='inactiveusers'),
    path('edituser/<int:id>/', views.edituser, name='edituser'),
    path('activateuser/<int:id>/', views.activateuser, name='activateuser'),
    path('edituser/<int:webuser_id>/deletesysuser/<int:sysuser_id>/', views.delete_sysuser_from_user, name='delete_sys_from_webuser'),
    path('jupyterhub', views.jupyterhub, name='jupyterhub'),
    path('mailview', views.mail_to_users, name='email_to_users'),
    path('userdata', views.userdata, name='userdata'),
    path('setpreferred/<int:sysuser_id>/', views.set_preferred_user, name='set_preferred')
]
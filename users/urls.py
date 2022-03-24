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
    path('registration', views.registration, name='registration'),
    path('systemuser', views.systemuser, name='systemuser'),
    path('users', views.users, name='users'),
    path('inactiveusers', views.inactiveusers, name='inactiveusers'),
    path('edituser/<int:id>/', views.edituser, name='edituser'),
    path('activateuser/<int:id>/', views.activateuser, name='activateuser'),
    path('edituser/<int:webuser_id>/deletesysuser/<int:sysuser_id>/', views.delete_sysuser_from_user, name='delete_sys_from_webuser'),
]
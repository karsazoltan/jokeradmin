
from django.urls import path, include
from rest_framework import routers

from . import views
from .restapi import SSHKeyViewSet

router = routers.DefaultRouter()
router.register(r'rest', SSHKeyViewSet)

urlpatterns = [
    path('sshkey/', include(router.urls)),
    path('sshkeys', views.sshkey, name='sshkeys'),
    path('sshkeys/activate/<int:id>/', views.activatekey, name='activatekey'),
    path('sshkeys/delete/<int:id>/', views.deletekey, name='deletekey'),
    path('sshkeys/admin/activate/<int:id>/', views.adminactivate, name='adminactivatekey'),
    path('sshkeys/admin/delete/<int:id>/', views.admindelete, name='admindeletekey'),
    path('sshkeys/admin', views.adminkeys, name='adminkeys')
]

from django.urls import path, include
from . import views

urlpatterns = [
    path('sshkeys', views.sshkey, name='sshkeys'),
    path('sshkeys/activate/<int:id>/', views.activatekey, name='activatekey'),
    path('sshkeys/delete/<int:id>/', views.deletekey, name='deletekey'),
    path('sshkeys/admin/activate/<int:id>/', views.adminactivate, name='adminactivatekey'),
    path('sshkeys/admin/delete/<int:id>/', views.admindelete, name='admindeletekey'),
    path('sshkeys/admin', views.adminkeys, name='adminkeys')
]
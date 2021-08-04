
from django.urls import path, include
from . import views

urlpatterns = [
    path('sshkeys', views.sshkey, name='sshkeys'),
    path('activatekey/<int:id>/', views.activatekey, name='activatekey'),
    path('deletekey/<int:id>/', views.deletekey, name='deletekey')
]
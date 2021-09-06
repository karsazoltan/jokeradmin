from django.urls import path
from . import views

urlpatterns = [
    path('user', views.userpage, name='user'),
    path('registration', views.registration, name='registration'),
    path('systemuser', views.systemuser, name='systemuser'),
    path('edituser/<int:id>/', views.edituser, name='edituser'),
]
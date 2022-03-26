from django.contrib.auth.models import User
from rest_framework import viewsets, filters
from rest_framework import permissions

from users.models import UserDetail, SystemUser
from users.serializers import UserSerializer, UserDetailSerializer, SystemUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get']
    filter_backends = [filters.SearchFilter]
    search_fields = ['^username', '^userdetail__neptun']


class UserDetailViewSet(viewsets.ModelViewSet):
    queryset = UserDetail.objects.all().order_by('-neptun')
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get']
    filter_backends = [filters.SearchFilter]
    search_fields = ['^neptun']


class SystemUserViewSet(viewsets.ModelViewSet):
    queryset = SystemUser.objects.all().order_by('-username')
    serializer_class = SystemUserSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get']
    filter_backends = [filters.SearchFilter]
    search_fields = ['^username']

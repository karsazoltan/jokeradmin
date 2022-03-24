from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import UserDetail, SystemUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'userdetail']


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserDetail
        fields = ['url', 'id', 'user', 'systemuser', 'neptun', 'description']


class SystemUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SystemUser
        fields = ['url', 'id', 'username', 'webusers']

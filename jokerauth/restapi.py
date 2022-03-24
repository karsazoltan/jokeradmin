from rest_framework import viewsets
from rest_framework import permissions
from jokerauth.models import SSHKey
from jokerauth.serializers import SSHKeySerializer


class SSHKeyViewSet(viewsets.ModelViewSet):
    queryset = SSHKey.objects.all().order_by('-create_date')
    serializer_class = SSHKeySerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get']
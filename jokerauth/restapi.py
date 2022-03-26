from rest_framework import viewsets, filters
from rest_framework import permissions
from jokerauth.models import SSHKey
from jokerauth.serializers import SSHKeySerializer


class SSHKeyViewSet(viewsets.ModelViewSet):
    queryset = SSHKey.objects.all().order_by('-create_date')
    serializer_class = SSHKeySerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get']
    filter_backends = [filters.SearchFilter]
    search_fields = ['^user__username', '^comment']

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }


from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from projects.models import Project
from projects.serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-create_date')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get']
    filter_backends = [filters.SearchFilter]
    search_fields = ['^owner__username', '^title']

from rest_framework import serializers

from projects.models import Project


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ['url', 'id', 'title', 'description', 'public', 'create_date', 'owner', 'users']

from rest_framework import serializers

from jokerauth.models import SSHKey


class SSHKeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SSHKey
        fields = ['url', 'id', 'user', 'create_date', 'pubkey', 'active', 'comment']
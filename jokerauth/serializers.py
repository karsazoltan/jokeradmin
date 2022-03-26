from django.urls import reverse
from rest_framework import serializers

from jokerauth.models import SSHKey


class SSHKeySerializer(serializers.HyperlinkedModelSerializer):
    active_url = serializers.SerializerMethodField('active_url_def')

    def active_url_def(self, key):
        return reverse('adminactivatekey', kwargs={'id': key.id})

    class Meta:
        model = SSHKey
        fields = ['url', 'id', 'user', 'create_date', 'pubkey', 'active', 'comment', 'active_url']
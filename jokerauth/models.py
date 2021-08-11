from django.db import models
from django.utils import timezone

from jokerauth.service import *


class SSHKey(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    pubkey = models.TextField(unique=True)
    active = models.BooleanField()
    comment = models.CharField(max_length=100, null=True)

    def addtoserver(self):
        if self.active is False:
            self.active = True
        else:
            self.active = False
        self.save()
        keys = SSHKey.objects.filter(user=self.user).filter(active=True)
        savekeys(keys, self.user)

    def deleteit(self):
        self.delete()
        keys = SSHKey.objects.filter(user=self.user).filter(active=True)
        savekeys(keys, self.user)

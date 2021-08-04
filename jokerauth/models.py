from django.db import models
from django.utils import timezone


class SSHKey(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    pubkey = models.TextField()
    active = models.BooleanField()
    comment = models.CharField(max_length=100, null=True)

    def addtoserver(self):
        if self.active is False:
            self.active = True
            # aktiválás
        else:
            self.active = False
            # törlés
        self.save()

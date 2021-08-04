from django.db import models


class UserDetail(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=False)
    email = models.CharField(max_length=200, null=False)
    name = models.CharField(max_length=200, null=False)
    systemuser = models.CharField(max_length=200, null=False)

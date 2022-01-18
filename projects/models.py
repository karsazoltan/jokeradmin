from django.utils import timezone
from django.db import models


class Project(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=False)
    users = models.ManyToManyField('auth.User', related_name='projects')
    system_user = models.OneToOneField('users.SystemUser', on_delete=models.CASCADE, null=True)
    create_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=1000, null=True)
    public = models.BooleanField()
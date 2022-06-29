from django.db import models

from users.service import is_sudo


class UserStatus(models.TextChoices):
    INACTIVE = 'IA', 'Inactive'
    REQUEST = 'RE', 'Request'
    OK = 'OK', 'OK'

class UserDetail(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=False)
    systemuser = models.ManyToManyField('SystemUser', related_name='webusers')
    description = models.CharField(max_length=500, null=True)
    status = models.CharField(
        max_length=2, choices=UserStatus.choices, default=UserStatus.INACTIVE
    )

    def issudo(self):
        if self.systemuser:
            return self.systemuser.issudo()
        else:
            return False


class SystemUser(models.Model):
    username = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.username

    def bashcmd(self):
        return f"sudo adduser -m -d /home1/{self.username.__str__()} {self.username.__str__()}"

    def issudo(self):
        return is_sudo(self.username)





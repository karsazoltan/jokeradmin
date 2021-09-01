from django.db import models


class UserDetail(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=False)
    systemuser = models.ForeignKey('SystemUser', on_delete=models.CASCADE, null=True)
    neptun = models.CharField(max_length=6, null=False, default='N3PTUN', unique=True)


# csak nem root
class SystemUser(models.Model):
    username = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.username

    def bashcmd(self):
        return f"sudo adduser -m -d /home1/{self.username.__str__()} {self.username.__str__()}"




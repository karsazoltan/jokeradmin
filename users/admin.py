from django.contrib import admin

# Register your models here.
from jokerauth.models import SSHKey
from projects.models import Project
from users.models import UserDetail

admin.site.register(SSHKey)
admin.site.register(Project)
admin.site.register(UserDetail)
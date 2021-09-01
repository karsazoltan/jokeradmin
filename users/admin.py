from django.contrib import admin
from .models import UserDetail, SystemUser

admin.site.register(UserDetail)
admin.site.register(SystemUser)
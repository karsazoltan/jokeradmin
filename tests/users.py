from unittest import TestCase

from django.contrib.auth.models import User


class UsersTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testuser')
        self.user.is_superuser = True
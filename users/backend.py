from djangosaml2.backends import Saml2Backend

from users.models import UserDetail, UserStatus


class ModifiedSaml2Backend(Saml2Backend):
    def save_user(self, user, *args, **kwargs):
        user.save()
        user_detail = UserDetail(user=user,
                                 description='',
                                 status=UserStatus.INACTIVE)
        user_detail.save()
        return super().save_user(user, *args, **kwargs)
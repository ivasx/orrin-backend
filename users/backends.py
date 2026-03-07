from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        login_field = username or kwargs.get(User.USERNAME_FIELD)

        if not login_field:
            return None

        try:
            user = User.objects.get(Q(username=login_field) | Q(email=login_field))
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
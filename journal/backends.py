# backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, sissy_name=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(sissy_name=sissy_name)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None

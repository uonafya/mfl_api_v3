from .models import MflUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import ModelBackend
from django.conf import settings


class MflUserAuthBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        """ Authenticate a user based on workforce_id / national_id. """
        try:
            print("Start", username, password)
            user = MflUser.objects.get(email__iexact=username.lower())
            if settings.ALLOW_EMPLOYEE_NUMBER_LOGIN:
                if not user:
                    user = MflUser.objects.get(employee_number=username)
            if user and check_password(password, user.password):
                return user
        except MflUser.DoesNotExist:
            print('ERROR')
            return None

    def get_user(self, user_id):
        """ Get a MflUser object from the user_id. """
        try:
            return MflUser.objects.get(pk=user_id)
        except MflUser.DoesNotExist:
            print('ERROR 2')
            return None
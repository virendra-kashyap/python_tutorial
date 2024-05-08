from django.contrib.auth.backends import BaseBackend
from django.shortcuts import get_object_or_404
from .models import Users

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = get_object_or_404(Users, emailId=email)
            if user.check_password(password):
                return user
        except Users.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None
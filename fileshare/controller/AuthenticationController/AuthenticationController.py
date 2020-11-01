from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class AuthenticationController:

    def checkLogin(self, username: str, password: str) -> User:
        user = User.objects.get(username=username)
        if user is not None:
            return user
        return None

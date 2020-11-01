from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class AuthenticationController:

    def checkLogin(self, email: str, password: str) -> User:
        user = authenticate(email=email, password=password)
        if user is not None:
            return user
        return None

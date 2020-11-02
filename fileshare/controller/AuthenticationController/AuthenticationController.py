from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from typing import Optional


class AuthenticationController:

    def __init__(self):
        print("Authentication Controller initialized")

    def checkLogin(self, username: str, password: str) -> Optional[User]:
        user = User.objects.get(username=username)
        if user is not None and user.password == password:
            return user
        return None


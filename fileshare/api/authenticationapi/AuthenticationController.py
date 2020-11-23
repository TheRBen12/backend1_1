from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from typing import Optional
from django.contrib import auth


class AuthenticationController:

    def __init__(self):
        print("Authentication Controller initialized")

    def checkLogin(self, request, username: str, password: str) -> Optional[User]:
        try:
            user = auth.authenticate(request, username=username, password=password)
            return user
        except User.DoesNotExist:
            print("no user with username")
            return None


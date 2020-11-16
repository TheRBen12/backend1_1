from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from typing import Optional
from django.contrib.auth.hashers import check_password


class AuthenticationController:

    def __init__(self):
        print("Authentication Controller initialized")

    def checkLogin(self, username: str, password: str) -> Optional[User]:
        try:
            user = User.objects.get(username=username)
            if(user.check_password(password)):
                return user
            else:
                print("incorrect password")
                return None
        except User.DoesNotExist:
            print("no user with username")
            return None


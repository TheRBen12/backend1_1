from django.contrib.auth.models import User
from passlib.context import CryptContext
from django.contrib.auth.hashers import make_password


class RegistrationController:

    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            default="pbkdf2_sha256",
            pbkdf2_sha256__default_rounds=30000)

    def checkIfEmailExists(self, email: str) -> bool:
        try:
            user = User.objects.get(email=email)
            return True
        except User.DoesNotExist:
            return False


from django.contrib.auth.models import User
from passlib.context import CryptContext


class RegistrationController:

    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            default="pbkdf2_sha256",
            pbkdf2_sha256__default_rounds=30000)

    def checkIfEmailExists(self, email: str) -> bool:
        user = User.objects.get(email=email)
        if user is not None:
            return True
        return False

    def hashPassword(self, password: str) -> str:
        return self.pwd_context.encrypt(password)

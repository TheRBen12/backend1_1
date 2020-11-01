from django.contrib.auth.models import User


class RegistrationController:

    def checkIfEmailExists(self, email: str) -> bool:
        user = User.objects.get(email=email)
        if user is not None:
            return True
        return False



from typing import List

from django.contrib.auth.models import User


class PersonController:

    def __init__(self):
        print("PersonController initialized")

    def newPerson(self, email, username, password):
        user = User.objects.create_user(username, email, password=password)
        user.save()
        return user

    def getPersonByEmail(self, email: str) -> User:
        return User.objects.get(email=email)

    def getPersonByid(self, id: int) -> User:
        return User.objects.get(id= id)

    def getAll(self) -> List[User]:
        return User.objects.all()


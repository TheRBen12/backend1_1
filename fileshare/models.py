from django.db import models
from django.contrib.auth.models import User
from typing import List


# Create your models here.


class PersonLogin(models.Model):
    person = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    loged_in = models.DateField()


class LoginState(models.Model):
    state = models.CharField(max_length=100)


class Group(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateField()
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Group name: {}, created_at: '{}' from {}".format(self.name, self.created_at, self.creator)


class PersonGroupMember(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    joined_at = models.DateField()

class InvitationReceiver(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    invitation = models.ForeignKey(Invitation, on_delete=models.DO_NOTHING)


class Invitation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    receivers: List[InvitationReceiver]
    created_at = models.DateField()


class FileType(models.Model):
    type = models.CharField(max_length=100)


class File(models.Model):
    name = models.CharField(max_length=100)
    uploaded_at = models.DateField()
    public = models.BooleanField()
    price = models.FloatField()
    type = models.ForeignKey(FileType, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField()
    size = models.IntegerField()


class FileSharePerson(models.Model):
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="creator")
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="receiver")
    file = models.ForeignKey(File, on_delete=models.DO_NOTHING)
    shared_at = models.DateField()


class FileShareGroup(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)






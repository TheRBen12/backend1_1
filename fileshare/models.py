from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class PersonLogin(models.Model):
    person = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    loged_in = models.DateField()


class Group(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateField()
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class PersonGroupMember(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    joined_at = models.DateField()


class Invitation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateField()


class InvitationReceiver(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    invitation = models.ForeignKey(Invitation, on_delete=models.DO_NOTHING)


class FileType(models.Model):
    type = models.CharField(max_length=100)


class File(models.Model):
    name = models.CharField(max_length=100)
    size = models.FloatField()
    uploaded_at = models.DateField()
    public = models.BooleanField()
    price = models.FloatField()
    type = models.ForeignKey(FileType, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField()


class FileSharePerson(models.Model):
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="creator")
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="receiver")
    file = models.ForeignKey(File, on_delete=models.DO_NOTHING)
    shared_at = models.DateField()


class FileShareGroup(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)



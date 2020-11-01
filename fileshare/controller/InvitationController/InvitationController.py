from fileshare.models import Invitation
from django.contrib.auth.models import User
from fileshare.models import Group
from datetime import datetime


class InvitationController:

    def newInvitation(self, senderid: int, groupid: int) -> Invitation:
        sender = User.objects.get(id=senderid)
        group = Group.objects.get(id=groupid)
        invitation = Invitation.objects.create(sender=sender, group=group, created_at=datetime.now())
        return invitation



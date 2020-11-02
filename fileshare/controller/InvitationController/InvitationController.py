from fileshare.models import Invitation, InvitationReceiver
from django.contrib.auth.models import User
from fileshare.models import Group
from datetime import datetime
from typing import List


class InvitationController:

    def __init__(self):
        print("Invitation Controller initialized")

    def newInvitation(self, receivers: List[InvitationReceiver], sender: int) -> Invitation:
        groupid = receivers[0].invitation.group_id
        for receiver in receivers:
            InvitationReceiver.objects.create(receiver_id=receiver.id, invitation_id=receiver.invitation.id)
        invitation = Invitation.objects.create(sender_id=sender, receivers=receivers, group_id=groupid)
        return invitation



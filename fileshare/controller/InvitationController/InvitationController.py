from fileshare.models import Invitation, InvitationReceiver

from typing import List


class InvitationController:

    def __init__(self):
        print("Invitation Controller initialized")

    def newInvitation(self, invitation: Invitation, sender: int) -> Invitation:
        for receiver in invitation.receivers:
            InvitationReceiver.objects.create(receiver_id=receiver.id, invitation_id=invitation.id)
        invitation = Invitation.objects.create(sender_id=sender, receivers=invitation.receivers, group_id=invitation.group)
        return invitation



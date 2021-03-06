from fileshare.models import Invitation, InvitationReceiver

from typing import List


class InvitationController:

    def __init__(self):
        print("Invitation Controller initialized")

    def newInvitation(self, invitation: Invitation, sender: int) -> Invitation:
        invitation = Invitation.objects.create(invitation)
        for receiver in invitation.receivers:
            InvitationReceiver.objects.create(receiver_id=receiver, invitation_id=invitation.id)
        invitation = Invitation.objects.create(sender_id=sender, receivers=invitation.receivers, group=invitation.group)
        return invitation



from datetime import datetime

from fileshare.models import Group
from typing import List, Dict


def getAll() -> List:
    return Group.objects.all()


class GroupController:
    def __init__(self):
        print('group controller initialized')

    def getAll(self) -> List:
        return Group.objects.all()

    def newGroup(self, group: Dict) -> Group:
        group = Group.objects.create(name=group['name'],
                                     creator_id=group['creator'], created_at=datetime.now())
        return group

    def updateGroup(self, group: Group) -> Group:
        group.save()
        return group

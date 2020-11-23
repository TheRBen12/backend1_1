from datetime import datetime
from fileshare.models import Group
from typing import List, Dict


class GroupController:
    def __init__(self):
        print('group controller initialized')

    def getAll(self) -> List:
        return Group.objects.all()

    def newGroup(self, name: str, creator: int) -> Group:
        group = Group.objects.create(name=name,
                                     creator_id=creator, created_at=datetime.now())
        return group

    def updateGroup(self, group: Group) -> Group:
        group = Group.objects.update(id=group.id)
        return group

    def deleteGroup(self, id: int):
        group = Group.objects.get(id=id)
        group.delete()
        return group

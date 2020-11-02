from fileshare.models import Group
from typing import List


def getAll() -> List:
    return Group.objects.all()


class GroupController:
    def __init__(self):
        print('group controller initialized')

    def getAll(self) -> List:
        return Group.objects.all()

    def newGroup(self, group: Group) -> Group:
        group.save()
        return group

    def updateGroup(self, group: Group) -> Group:
        group.save()
        return group

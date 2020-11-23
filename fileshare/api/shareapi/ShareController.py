from datetime import datetime
from datetime import date
from typing import Optional

from fileshare.models import FileSharePerson


class ShareController:
    def __init__(self):
        print("Share Controller initialized")

    def newShareFilePerson(self, sender: int, receiver: int, file: int) -> Optional[FileSharePerson]:
        sharedFile_ = FileSharePerson.objects.filter(receiver_id=receiver).exists()
        if sharedFile_:
            return None
        else:
            return FileSharePerson.objects.create(receiver_id=receiver, creator_id=sender, file_id=file, shared_at=date.today())

        pass

    def getSharedFilesByPerson(self, receiver: int):
        list = FileSharePerson.objects.last()
        sharedFiles = [sharedFile.file for sharedFile in FileSharePerson.objects.all() if sharedFile.receiver.id == receiver]
        return sharedFiles
        pass

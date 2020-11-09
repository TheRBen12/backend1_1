from fileshare.models import File
from typing import List
from datetime import datetime


class FileController:

    def getAllFiles(self) -> List[File]:
        return File.objects.all()

    def newFile(self, file: File, owner, typeid: int) -> File:
        file = File.objects.create(file=file, owner=owner, size=file.size,
                                   public=False, uploaded_at=datetime.now(),
                                   name=file.name, price=0.0, type_id=typeid)


        return file

    def updateFile(self, file: File) -> File:
        file = File.objects.update(file)
        return file

    def checkFileSize(self, file: File) -> bool:
        if file.size > 100000:
            return False
        return True

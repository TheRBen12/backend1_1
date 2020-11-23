from fileshare.models import File, FileType
from typing import List, Dict
from datetime import datetime


class FileController:

    def __init__(self):
        print("File controller initialized")

    def getAllFiles(self) -> List[File]:
        return File.objects.all()

    def getFileById(self, id: int):
        return File.objects.get(id=id)

    def newFile(self, file: File, owner, price, type: FileType) -> File:
        file = File.objects.create(file=file, owner=owner, size=file.size,
                                   public=False, uploaded_at=datetime.now(),
                                   name=file.name, price=price, type=type)

        return file

    def updateFile(self, file_: File) -> File:
        file = File.objects.get(id=file_.id)
        file.public = file_.public
        file.name = file_.name
        file.owner = file_.owner
        file.save()
        return file

    def checkFileSize(self, file: File) -> bool:
        if file.size > 100000:
            return False
        return True

    def setPublicity(self, publicity: int):
        if publicity == 1:
            return True
        return False

    def getFileType(self, typeName: str) -> FileType:
        n = FileType.objects.filter(type=typeName)
        if len(n) > 0:
            return FileType.objects.get(type=typeName)
        else:
            type = self.newFileType(typeName)
            return type

    def newFileType(self, typeName) -> FileType:
        return FileType.objects.create(type=typeName)

    def deleteFile(self, id: int):
        file = File.objects.get(id=id)
        file.delete()
        return file
        pass

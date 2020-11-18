from fileshare.models import File, FileType
from typing import List
from datetime import datetime


class FileController:

    def __init__(self):
        print("File controller initialized")

    def getAllFiles(self) -> List[File]:
        return File.objects.all()

    def newFile(self, file: File, owner, type: FileType) -> File:
        file = File.objects.create(file=file, owner=owner, size=file.size,
                                   public=False, uploaded_at=datetime.now(),
                                   name=file.name, price=0.0, type=type)


        return file

    def updateFile(self, file: File) -> File:
        file = File.objects.update(file)
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
            type = self.newType(typeName)
            return type


    def newFileType(self, typeName) -> FileType:
        return FileType.objects.create(type=typeName)

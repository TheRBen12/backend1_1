from fileshare.models import File
from typing import List


class FileController:

    def getAllFiles(self) -> List[File]:
        return File.objects.all()

    def newFile(self, file: File, owner) -> File:
        file = File.objects.create(file=file, owner=owner)
        return file

    def updateFile(self, file: File) -> File:
        file = File.objects.update(file)
        return file


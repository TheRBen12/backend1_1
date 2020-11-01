from fileshare.models import File
from typing import List


class FileController:

    def getAllFiles(self) -> List[File]:
        return File.objects.all()

    def newFile(self, file: File):
        file = File.objects.create(file)
        return file

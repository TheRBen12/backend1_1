from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from fileshare.models import File, FileType, FileSharePerson
import json
from fileshare.views import newFile, updateFile, deleteFile, getFilesByOwnerId, ShareView
from django.core.files.uploadedfile import SimpleUploadedFile


# All unit tests are implemented here.


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.all().delete()

    def test_register_post_request(self):
        response = self.client.post('/register/', {'username': 'admin', 'password': 'admin', 'email': 'admin@ad.ch'})
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        self.assertEqual(response['username'], User.objects.get(username='admin').username)
        self.email_already_exist()

    def email_already_exist(self):
        response = self.client.post('/register/', {'username': 'mueller', 'password': 'test', 'email': 'admin@ad.ch'})
        content = str(response.content.decode())
        self.assertEqual(content, '"Email already exists"')


class LoginTestCase(TestCase):
    def setUp(self):
        FileSharePerson.objects.all().delete()
        User.objects.all().delete()
        self.client = Client()
        self.createUser()

    def createUser(self):
        User.objects.create(username='admin', password='admin')

    def test_login_case(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.get(username='admin').is_active)


class FileTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        User.objects.create(username='admin', email='admin@ad.ch', password='admin')
        self.fileType = FileType.objects.create(type='application/pdf')
        self.new_file()

    def test_new_file_post_request(self):
        owner = User.objects.last().id
        current_amount_files = len(File.objects.all())
        file = None
        with open('fileshare/Studie.docx', 'rb') as f:
            file = SimpleUploadedFile("Studie.docx", f.read())
        request = self.factory.post('/newfile/', data={'owner': owner, 'state': 1})
        request.FILES['file'] = file
        response = newFile(request=request)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        next_current_amount_files = len(File.objects.all())
        self.assertTrue(response['id'], not None)
        self.assertTrue(next_current_amount_files > current_amount_files)

    def test_update_file(self):
        current_amount_public_files = len([file for file in File.objects.all() if file.public])
        file = File.objects.last()
        file.public = False
        request = self.factory.put('/updatefile/')
        request.FILES['files'] = file
        response = updateFile(request=request)
        next_current_amount_public_files = len([file for file in File.objects.all() if file.public])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(next_current_amount_public_files < current_amount_public_files)

    def test_delete_file(self):
        current_amount_public_files = len([file for file in File.objects.all()])
        id = File.objects.last().id
        request = self.factory.post('/deletefile/', data={'id': id})
        response = deleteFile(request=request)
        next_current_amount_public_files = len([file for file in File.objects.all()])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(next_current_amount_public_files == current_amount_public_files - 1)

    def test_own_files(self):
        ownerid = User.objects.last().id
        print(File.objects.last().owner.id)
        request = self.factory.get('/ownfiles/', data={'ownerid': ownerid})
        response = getFilesByOwnerId(request=request)
        response = json.loads(response.content.decode())
        self.assertTrue(response[0].id == ownerid)

    def new_file(self):
        File.objects.create(file='Studie.docx', name="Studie", uploaded_at=datetime.now(),
                            owner=User.objects.last(), price=0.0, public=True, type=self.fileType, size=0.0)


class GroupTestcase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User.objects.create(username='admin', email='admin@ad.ch', password='admin')


class ShareFilePersonCase(TestCase):
    def setUp(self):
        FileSharePerson.objects.all().delete()
        FileType.objects.all().delete()
        FileType.objects.create(type='application/pdf')
        File.objects.all().delete()
        User.objects.all().delete()
        User.objects.create(username='admin', password='admin')
        User.objects.create(username='admin1', password='admin1')
        self.factory = RequestFactory()
        self.shareView = ShareView()
        with open('fileshare/testfiles/Studie.docx', 'rb') as f:
            file = SimpleUploadedFile("Studie.docx", f.read())
            File.objects.create(file=file, owner=User.objects.last(), type=FileType.objects.last(), size=0.0,
                                uploaded_at=datetime.now(),
                                name="Test", public=False, price=10.0)

    def test_share_file_person(self):
        personid = User.objects.get(username='admin').id
        current_amount_sharedFiles = len([sharedFile for sharedFile in FileSharePerson.objects.all() if sharedFile.receiver.id == personid])
        request = self.factory.post('/sharefileperson/',
                                    data={'receiver': User.objects.get(username='admin').id,
                                          'creator': User.objects.get(username='admin1').id,
                                          'file': File.objects.last().id})
        response = self.shareView.shareFilePerson(request=request)
        next_current_amount_sharedFiles = len([sharedFile for sharedFile in FileSharePerson.objects.all() if sharedFile.receiver.id == personid])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(next_current_amount_sharedFiles > current_amount_sharedFiles)

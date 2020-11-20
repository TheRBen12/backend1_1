from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from fileshare.models import File, FileType
import json


# Create your tests here.

# unit tests for the backend are going to be implemented here

class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_post_request(self):
        response = self.client.post('/register/', {'username': 'admin', 'password': 'admin', 'email': 'admin@ad.ch'})
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        self.assertEqual(response['username'], User.objects.get(username='admin').username)
        self.email_already_exist()

    def email_already_exist(self):
        response = self.client.post('/register/', {'username': 'mueller', 'password': 'test', 'email': 'admin@ad.ch'})
        print(response.content.decode())
        content = response.content.decode()
        self.assertEqual(content, 'email already exists')


class LoginTestCase(TestCase):
    def setUp(self):
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
        self.file = None
        User.objects.create(username='admin', email='admin@ad.ch', password='admin')
        self.fileType = FileType.objects.create(type= 'application/pdf')

    def test_new_file_type(self):
        self.assertTrue(self.fileType is not None)

    def test_new_file_post_request(self):
        self.file = self.new_file()
        self.assertTrue(self.file is not None)
        self.assertEqual(self.file.owner.username, 'admin')
        self.assertEqual(self.file.public, True)

    def test_update_File(self):
        files = [file for file in File.objects.all() if file.public]
        current_amount_public_files = len(files)
        response = self.client.post('/updatefile/', self.file)

    def new_file(self) -> File:
        file = File.objects.create(file='../pics/Studie.docx', name="Studie", uploaded_at=datetime.now(),
                                   owner=User.objects.last()
                                   , price=0.0, public=True, type=self.fileType, size=0.0)
        return file


class GroupTestcase(TestCase):
    def setUp(self):
        self.client = Client()

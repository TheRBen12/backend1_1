import os
from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from requests import Response
import requests
from fileshare.api.fileapi.FileController import FileController
from fileshare.models import File, FileType
import json
from fileshare.views import newFile, updateFile
from django.core.files.uploadedfile import SimpleUploadedFile


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
        self.factory = RequestFactory()
        User.objects.create(username='admin', email='admin@ad.ch', password='admin')
        self.fileType = FileType.objects.create(type='application/pdf')
        self.new_file()

    def test_new_file_post_request(self):
        owner = User.objects.last().id
        current_amount_files = len(File.objects.all())
        file = open('fileshare/Studie.docx', 'r')
        file = File(file)
        request = self.factory.post('/newfile/', data={'owner': owner, 'state': 1})
        request.FILES['files'] = file
        response = newFile(request=request)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        self.assertTrue(response['id'], not None)
        next_current_amount_files = len(File.objects.all())
        self.assertTrue(next_current_amount_files > current_amount_files)

    def test_update_file(self):
        file = File.objects.last()
        file.public = False
        request = self.factory.put('/updatefile/')
        request.FILES['files'] = file
        response = updateFile(request=request)

    def new_file(self):
        file = File.objects.create(file='Studie.docx', name="Studie", uploaded_at=datetime.now(),
                                   owner=User.objects.last()
                                   , price=0.0, public=True, type=self.fileType, size=0.0)


class GroupTestcase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User.objects.create(username='admin', email='admin@ad.ch', password='admin')



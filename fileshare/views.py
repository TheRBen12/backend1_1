
from django.contrib.auth import  login
from django.http import HttpResponse
from .models import File
from .controller.RegistrationController.RegistrationController import RegistrationController
from .controller.PersonController.PersonController import PersonController
from .controller.AuthenticationController.AuthenticationController import AuthenticationController
from .controller.FileController.FileController import FileController
from .serializer.modelserializers import PersonSerializer, FileSerializer
from rest_framework import serializers
from datetime import datetime


# Controllers
registerController = RegistrationController()
personController = PersonController()
authenticationController = AuthenticationController()
fileController = FileController()


# --------------------------#Personapi#----------------------------
def register(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not registerController.checkIfEmailExists(email):
        user = personController.newPerson(email, username, password)
        serializer = PersonSerializer(user)
        print('serialized data:', serializer.data)
        response = HttpResponse(serializer.data)
        response['Content-Type'] = 'application/json'
        response['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        return HttpResponse('login failed')


def authenticate(request, response):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticationController.checkLogin(email, password)
    if user is not None:
        request.session['user'] = user.id
        login(request, user)
        response.set_cookie('user', user.id)
        return response


def displayPersonByEmail(request):
    email = request.POST.get('email')
    user = personController.getPersonByEmail(email)
    serializer = PersonSerializer(user)
    response = HttpResponse(serializer.data)
    response['Content-Type'] = 'application/json'
    response['Access-Control-Allow-Origin'] = '*'
    return response


# ------------------------------#Fileapi#-------------------------

def newFile(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file = fileController.newFile(file)
        serializer = FileSerializer(file)
        response = serializer.data
        response = HttpResponse(response)
        response['Content-Type'] = 'multipart/form-data'
        response['Access-Control-Allow-Origin'] = '*'
        return response


def displayAllFiles(request):
    files = fileController.getAllFiles()
    json = serializers.serialize('json', files)
    print(json)
    response = HttpResponse(files)
    response['Content-Type'] = 'application/json'
    response['Access-Control-Allow-Origin'] = '*'
    return response



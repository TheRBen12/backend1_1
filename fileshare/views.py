from typing import Dict

from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from .api.personapi.RegistrationController import RegistrationController
from .api.personapi.PersonController import PersonController
from .api.authenticationapi.AuthenticationController import AuthenticationController
from .api.fileapi.FileController import FileController
from .api.groupapi.GroupController import GroupController
from .api.invitationapi.InvitationController import InvitationController
from .api.shareapi.ShareController import ShareController
from .serializer.modelserializers import PersonSerializer, FileSerializer, GroupSerializer, ShareFilePersonSerializer
import json
from django.views.decorators.csrf import csrf_exempt

# Controllers
registerController = RegistrationController()
personController = PersonController()
authenticationController = AuthenticationController()
fileController = FileController()
groupController = GroupController()
invitationController = InvitationController()
shareController = ShareController()


# --------------------------#Personapi#----------------------------
@csrf_exempt
def register(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not registerController.checkIfEmailExists(email):
        person = personController.newPerson(email, username, password)
        user = auth.authenticate(request, username=username, password=password)
        auth.login(request, user)
        serializer = PersonSerializer(person)
        print('serialized data:', serializer.data)
        response = JsonResponse(serializer.data)
        return response
    else:
        return JsonResponse('Email already exists', safe=False)


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticationController.checkLogin(request, username, password)
    if user:
        auth.login(request, user)
        print(request.user.id)
        serializer = PersonSerializer(user)
        response = JsonResponse(serializer.data, safe=False)
        response.set_cookie('user', user.id, expires=None)
        return response
    else:
        return JsonResponse('login failed', safe=False)

@csrf_exempt
def logout(request):
    auth.logout(request)
    return JsonResponse("logged out", safe=False)


def displayPersonByEmail(request):
    email = request.POST.get('email')
    user = personController.getPersonByEmail(email)
    serializer = PersonSerializer(user)
    response = HttpResponse(serializer.data)
    response['Content-Type'] = 'application/json'
    response['Access-Control-Allow-Origin'] = '*'
    return response


def displayAllPersons(request):
    persons = personController.getAll()
    serializer = PersonSerializer(persons, many=True)
    response = JsonResponse(serializer.data, safe=False)
    response['Content-Type'] = 'application/json'
    response['Access-Control-Allow-Origin'] = '*'
    return response


# ------------------------------#Fileapi#-------------------------

def newFile(request):
    file = request.FILES['file']
    typeName = file.content_type
    type = fileController.getFileType(typeName)
    owner = personController.getPersonByid(int(request.POST.get('owner')))
    price = request.POST.get('price')
    file = fileController.newFile(file, owner, price, type)
    if file:
        file.public = fileController.setPublicity(int(request.POST.get('state')))
        file.save()
        serializer = FileSerializer(file)
        response = JsonResponse(serializer.data)
        return response
    else:
        response = JsonResponse(file, safe=False)
        return response



@csrf_exempt
def displayAllPublicFiles(request):
    files = fileController.getAllFiles()
    files = [file for file in files if file.public == 1]
    serializer = FileSerializer(files, many=True)
    response = JsonResponse(serializer.data, safe=False)
    response['Content-Type'] = 'application/json'
    response['Access-Control-Allow-Origin'] = '*'
    return response

def displayAllAccessableFiles(request, id):
    id = int(id)
    files = fileController.getAllFiles()
    files = [file for file in files if file.public == 1 or file.owner.id == id]
    files = files + shareController.getSharedFilesByPerson(id)
    serializer = FileSerializer(files, many=True)
    response = JsonResponse(serializer.data, safe=False)
    response['Content-Type'] = 'application/json'
    return response

def displayCartFiles(request):
    cartContent = request.POST.get("ids")
    ids = cartContent.split(";")
    print("ids", ids)
    files = fileController.getAllFiles()
    files = [file for file in files if str(file.id) in ids]
    serializer = FileSerializer(files, many=True)
    response = JsonResponse(serializer.data, safe=False)
    response['Content-Type'] = 'application/json'
    response['Access-Control-Allow-Origin'] = '*'
    return response


def getFilesByOwnerId(request, id):
    id = int(id)
    files = [file for file in fileController.getAllFiles() if file.owner.id == id]
    serializer = FileSerializer(files, many=True)
    response = JsonResponse(serializer.data, safe=False)
    response['Content-Type'] = 'application/json'
    response['Access-Control-Allow-Origin'] = '*'
    return response


def updateFile(request):
    file = request.FILES['files']
    file = fileController.updateFile(file)
    serializer = FileSerializer(file)
    response = JsonResponse(serializer.data)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def deleteFile(request, id):
    id = int(id)
    file = fileController.getFileById(id)
    fileController.deleteFile(id)
    serializer = FileSerializer(file)
    response = JsonResponse(serializer.data)
    return response


# ----------------------#GroupApi#----------------------

def newGroup(request):
    group = groupController.newGroup(request.POST.get('name'), int(request.POST.get('creator')))
    serializer = GroupSerializer(group)
    response = JsonResponse(serializer.data)
    response['Content-Type'] = 'application/json'
    response['Access-Control-Allow-Origin'] = '*'
    return response


def displayAllGroups():
    groups = groupController.getAll()
    serializer = GroupSerializer(groups, many=True)
    result = serializer.data
    print('All groups:', result)
    response = JsonResponse(serializer.data)
    return response


# ---------------#InvitatinController#-----------

def newInvitation(request):
    invitation = request.body
    sender = request.session.get("user")
    invitation = invitationController.newInvitation(invitation, sender)
    response = JsonResponse(invitation)
    return response


def updateInvitation(request):
    return None


# ----------------#ShareApi-------------------------------


class ShareView:

    def shareFilePerson(self, request):
        fileId = request.POST.get('file')
        receiver = request.POST.get('receiver')
        sender = request.POST.get('creator')
        shared = shareController.newShareFilePerson(sender, receiver, fileId)
        if shared is not None:
            serializer = ShareFilePersonSerializer(shared)
            response = JsonResponse(serializer.data, safe=False)
            return response
        else:
            return JsonResponse('error-already-shared', safe=False)

    def getSharedFilesByPerson(self, request, id):
        id = int(id)
        sharedFiles = shareController.getSharedFilesByPerson(id)
        serializer = FileSerializer(sharedFiles, many=True)
        response = JsonResponse(serializer.data, safe=False)
        return response

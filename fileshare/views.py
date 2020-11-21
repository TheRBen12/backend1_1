from typing import Dict

from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from .api.personapi.RegistrationController import RegistrationController
from .api.personapi.PersonController import PersonController
from .api.authenticationapi.AuthenticationController import AuthenticationController
from .api.fileapi.FileController import FileController
from .api.groupapi.GroupController import GroupController
from .api.invitationapi.InvitationController import InvitationController
from .serializer.modelserializers import PersonSerializer, FileSerializer, GroupSerializer
import json
from django.views.decorators.csrf import csrf_exempt

# Controllers
registerController = RegistrationController()
personController = PersonController()
authenticationController = AuthenticationController()
fileController = FileController()
groupController = GroupController()
invitationController = InvitationController()


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
        # request.session['user'] = person.id
        print('serialized data:', serializer.data)
        response = JsonResponse(serializer.data)
        return response
    else:
        return JsonResponse('Email already exists')


@csrf_exempt
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
        auth.login(request, user)
        print(request.user.id)
        serializer = PersonSerializer(user)
        response = JsonResponse(serializer.data)
        response.set_cookie('user', user.id, expires=None)
        return response
    else:
        return JsonResponse('login failed')


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


# ------------------------------#Fileapi#-------------------------

def newFile(request):
    file = request.FILES['files']
    typeName = file.content_type
    type = fileController.getFileType(typeName)
    owner = personController.getPersonByid(int(request.POST.get('owner')))
    file = fileController.newFile(file, owner, type)
    file.public = fileController.setPublicity(int(request.POST.get('state')))
    file.save()
    serializer = FileSerializer(file)
    response = JsonResponse(serializer.data)
    return response

@csrf_exempt
def displayAllPublicFiles(request):
    files = fileController.getAllFiles()
    files = [file for file in files if file.public==1]
    serializer = FileSerializer(files, many=True)
    response = JsonResponse(serializer.data, safe=False)
    response['Content-Type'] = 'application/json'
    response['Access-Control-Allow-Origin'] = '*'
    return response


def getFilesByOwnerId(request):
    print("came here")
    print(request.user)
    id = request.user.id
    print(id)
    files = [file for file in fileController.getAllFiles() if file.owner.id == id]
    serializer = FileSerializer(files, many=True)
    # print('All files:', serializer.data)
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
    return None


# ----------------------#GroupApi#----------------------

def newGroup(request):
    data = json.loads(request.body)
    group = groupController.newGroup(data)
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

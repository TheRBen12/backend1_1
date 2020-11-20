from django.contrib.auth import login
from django.http import HttpResponse, JsonResponse
from .api.personapi.RegistrationController import RegistrationController
from .api.personapi.PersonController import PersonController
from .api.authenticationapi.AuthenticationController import AuthenticationController
from .api.fileapi.FileController import FileController
from .api.groupapi.GroupController import GroupController
from .api.invitationapi.InvitationController import InvitationController
from .serializer.modelserializers import PersonSerializer, FileSerializer, GroupSerializer
import json


# Controllers
registerController = RegistrationController()
personController = PersonController()
authenticationController = AuthenticationController()
fileController = FileController()
groupController = GroupController()
invitationController = InvitationController()


# --------------------------#Personapi#----------------------------
# @csrf_exempt
def register(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')

    if not registerController.checkIfEmailExists(email):
        person = personController.newPerson(email, username, password)
        serializer = PersonSerializer(person)
        print('serialized data:', serializer.data)
        response = JsonResponse(serializer.data)
        return response
    else:
        return HttpResponse('Email already exists')


def authenticate(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticationController.checkLogin(username, password)
    if user is not None:
        login(request, user)
        serializer = PersonSerializer(user)
        response = JsonResponse(serializer.data)
        request.session['user'] = user.id
        response.set_cookie('user', user.id, expires=None)
        return response
    else:
        return HttpResponse('login failed')


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
    file = request.FILES['file']
    typeName = file.content_type
    type = fileController.getFileType(typeName)
    owner = personController.getPersonByid(int(request.POST.get('owner')))
    file = fileController.newFile(file, owner, type)
    file.public = fileController.setPublicity(int(request.POST.get('state')))
    file.save()
    serializer = FileSerializer(file)
    response = JsonResponse(serializer.data)
    return response


def displayAllPublicFiles(request):
    files = fileController.getAllFiles()
    files = [file for file in files if file.public]
    serializer = FileSerializer(files, many=True)
    result = serializer.data
    print('All files:', result)
    response = HttpResponse(files)
    response['Content-Type'] = 'application/json'
    response['Access-Control-Allow-Origin'] = '*'
    return response


def getFilesByOwnerId(request):
    id = request.session.get("user")
    files = [file for file in fileController.getAllFiles() if file.owner.id == id]
    serializer = FileSerializer(files, many=True)
    print('All files:', serializer.data)
    response = HttpResponse(serializer.data)
    response['Content-Type'] = 'application/json'
    response['Access-Control-Allow-Origin'] = '*'
    return response


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
    return response;


# ---------------#InvitatinController#-----------

def newInvitation(request):
    invitation = request.body
    sender = request.session.get("user")
    invitation = invitationController.newInvitation(invitation, sender)
    response = JsonResponse(invitation)
    return response


def updateInvitation(request):
    return None

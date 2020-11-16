from django.contrib.auth import login
from django.http import HttpResponse, JsonResponse
from .controller.RegistrationController.RegistrationController import RegistrationController
from .controller.PersonController.PersonController import PersonController
from .controller.AuthenticationController.AuthenticationController import AuthenticationController
from .controller.FileController.FileController import FileController
from .controller.GroupController.GroupController import GroupController
from .controller.InvitationController.InvitationController import InvitationController
from .serializer.modelserializers import PersonSerializer, FileSerializer, GroupSerializer

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
        return HttpResponse('sign up failed')


def authenticate(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticationController.checkLogin(username, password)
    print('user', user)
    if user is not None:
        request.session['user'] = user.id
        login(request, user)
        serializer = PersonSerializer(user)
        response = JsonResponse(serializer.data)
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
    owner = personController.getPersonByid(int(request.POST.get('owner')))
    typeid = int(request.POST.get('type'))
    file = fileController.newFile(file, owner, typeid)
    serializer = FileSerializer(file)
    response = JsonResponse(serializer.data)
    return response


def displayAllFiles(request):
    files = fileController.getAllFiles()
    serializer = FileSerializer(files, many=True)
    result = serializer.data
    print('All files:', result)
    response = HttpResponse(files)
    response['Content-Type'] = 'application/json'
    response['Access-Control-Allow-Origin'] = '*'
    return response


# ----------------------#GroupApi#----------------------

def newGroup(request):
    group = request.body
    group = groupController.newGroup(group)
    serializer = GroupSerializer(group)
    response = HttpResponse(serializer.data)
    response['Content-Type'] = 'application/json'
    response['Access-Control-Allow-Origin'] = '*'
    return response


# ---------------#InvitatinController#-----------

def newInvitation(request):
    invitation = request.body
    sender = request.session.get('user')
    invitation = invitationController.newInvitation(invitation, sender)


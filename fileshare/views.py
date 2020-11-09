from django.contrib.auth import login
from django.http import HttpResponse
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
def register(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not registerController.checkIfEmailExists(email):
        person = personController.newPerson(email, username, registerController.hashPassword(password))
        serializer = PersonSerializer(person)
        print('serialized data:', serializer.data)
        response = HttpResponse(serializer.data)
        response['Content-Type'] = 'application/json'
        response['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        return HttpResponse('login failed')


def authenticate(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    user = authenticationController.checkLogin(username, password)
    if user is not None:
        request.session['user'] = user.id
        login(request, user)
        serializer = PersonSerializer(user)
        response = HttpResponse(serializer.data)
        response.set_cookie('user', user.id)
        response['Content-Type'] = 'application/json'
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
    if request.method == 'POST' and request.session.get('user') is not None:
        file = request.FILES['file']
        ownerid = request.POST.get('user')
        owner = personController.getPersonByid(ownerid)
        file = fileController.newFile(file, owner)
        serializer = FileSerializer(file)
        response = serializer.data
        response = HttpResponse(response)
        response['Content-Type'] = 'multipart/form-data'
        response['Access-Control-Allow-Origin'] = '*'
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
    invitationReceivers = request.body
    sender = request.session.get('user')
    invitation = invitationController.newInvitation(invitationReceivers, sender)

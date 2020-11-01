from django.conf.urls import url
from . import views
urlpatterns = [
    url('register', views.register, name='register'),
    url('login', views.authenticate, name='login'),
    url('newfile', views.newFile, name='newFile'),
    url('files', views.displayAllFiles, name='displayAllFiles')
]
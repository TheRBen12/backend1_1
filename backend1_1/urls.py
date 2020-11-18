"""backend1_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from fileshare import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register),
    path('login/', views.authenticate),
    #path('person/delete/', views.deletePerson),
    path('newfile/', views.newFile),
    path('group/', views.newGroup),
    path('allfiles/', views.displayAllPublicFiles),
    path('ownfiles/', views.getFilesByOwnerId)

    #path('login/', include(('fileshare.urls', 'fileshare'), namespace='fileshare')),
    #path('newFile/', include(('fileshare.urls', 'fileshare'), namespace='fileshare')),
    #path('file/', include(('fileshare.urls', 'fileshare'), namespace='fileshare')),


    #url(r'^login/', include(('fileshare.urls', 'fileshare'), namespace='fileshare')),
    #url(r'^newfile/', include(('fileshare.urls', 'fileshare'), namespace='fileshare')),
    #url(r'^files/', include(('fileshare.urls', 'fileshare'), namespace='fileshare'))



]

from django.contrib import admin
from django.urls import path
from fileshare import views
from fileshare.views import ShareView

shareView = ShareView()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('newfile/', views.newFile),
    path('file/delete/<str:id>/', views.deleteFile),
    path('newgroup/', views.newGroup),
    path('allfiles/<str:id>/', views.displayAllAccessableFiles),
    path('updatefile/', views.updateFile),
    path('ownfiles/<str:id>/', views.getFilesByOwnerId),
    path('allpersons', views.displayAllPersons),
    path('sharefileperson/', shareView.shareFilePerson),
    path('sharefileperson/<str:id>/', shareView.getSharedFilesByPerson),
    path('cartfiles/', views.displayCartFiles)
]

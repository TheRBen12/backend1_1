# backend1_1: new backend1_1 working 
#if tables are not created automatically, please enter the following commands in the 
#commandline: 1) python manage.py makemigrations fileshare, 2) python manage.py migrate

#Start server and check the urls in /backend1_1/urls; these are the addresses you need to use 
#to touch the server 
              
#Note: Files from client must be sent as a form data 

#Note: each request which is sent to create a new Invitation must contain a body with a list 
#of InvitationReceiver objects (vgl. models) each receiver element in the list must contain a InvitationObject (vgl. models)

#Note: each object which is sent needs a userid to identify the owner of the ressource 



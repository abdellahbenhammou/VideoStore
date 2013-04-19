# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login

def login_u(request):
    message = "Please make sure you login"
    email = password = zaza =''
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username = email, password = password)
        zaza = user.email
        if user is not None:
            if user.is_active:
                login(request, user)
                message = "This is good, you are in "
            else:
                message = "You are not Active"
        else:
            message="Wrong Credentials, please retry again"
    return  render_to_response('auth.html', {'message':message, 'email':zaza})
# Create your views here.
from datetime import date
from django.shortcuts import render_to_response
from VideoStoreApp.models import User
from VideoStoreApp.models import Sessions
from VideoStoreApp.models import Video
from VideoStoreApp.forms import UploadForm
from django.db import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import os, tempfile
from django.contrib.sessions.models import Session
import os, string
from django.template.loader import render_to_string

def login(request):
    if "session_id" in request.COOKIES.keys():
        s=Sessions.objects.filter(session_id = request.COOKIES.get('session_id'))
        if s.count() == 0:
            message = "Incorrect Credentials, please retry"
            email = password = ''

            if request.POST:
                email = request.POST.get('email')
                password = request.POST.get('password')
                user = None
                try:
                #user = User(email=email, password=password)
                    user = User.objects.get(email = email, password = password)
                    message = email
                    #HttpResponseRedirect(reverse('VideoStoreApp.views.DisplayVideos'))
                    video_list = Video.objects.all()
                    ran = generate_random_string()
                    session = Sessions(session_id = ran)
                    session.save()
                    html = render_to_string('VideoStore.html', {'message': message, 'videos': video_list})
                    res = HttpResponse(html)
                    res.set_cookie('session_id', ran)
                    return res
                #user.objects
                except:

                    message = "Incorrect Credentials, please retry"
                    return render_to_response('auth.html', {'message': message})


            return render_to_response('auth.html', {'message': message})
    else:
        if request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = None
            try:
            #user = User(email=email, password=password)
                user = User.objects.get(email = email, password = password)
                message = email
                #HttpResponseRedirect(reverse('VideoStoreApp.views.DisplayVideos'))
                video_list = Video.objects.all()
                ran = generate_random_string()
                session = Sessions(session_id = ran)
                session.save()
                html = render_to_string('VideoStore.html', {'message': message, 'videos': video_list})
                res = HttpResponse(html)
                res.set_cookie('session_id', ran)
                return res
            #user.objects
            except:

                message = "Incorrect Credentials, please retry"
                return render_to_response('auth.html', {'message': message})
        return HttpResponseRedirect(reverse('VideoStoreApp.views.HomePage'))
    return HttpResponseRedirect(reverse('VideoStoreApp.views.HomePage'))


def Logout(request):

    Sessions.objects.filter(session_id = request.COOKIES['session_id']).delete()
    return render_to_response('auth.html')

def register(request):
    email = ''
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')

        newUser = User(email = email, password = password)
        newUser.save()
        return render_to_response('good.html', {'message':email})

    return render_to_response('register.html')

def writeFile(f, name_path):
    with open('store/'+name_path, 'wb+') as location:
        for byte in f.chunks():
            location.write(byte)


def videoUpload(request):
    if "session_id" in request.COOKIES.keys():
        s=Sessions.objects.filter(session_id = request.COOKIES.get('session_id'))
        if s.count()> 0:
            name_path = ''
            if request.method == 'POST':
                form = UploadForm(request.POST, request.FILES)
                if form.is_valid():
                    #name_path = request.POST.get('name')
                    name_path = request.FILES['file'].name
                    writeFile(request.FILES['file'], name_path)
                    video = Video(name= request.POST.get('name'),category=request.POST.get('cat'), rating=request.POST.get('rating'),
                                  remarks=request.POST.get('rem'), timeOfUpload=datetime.datetime.now(),path=name_path)
                    video.save()
                    return HttpResponseRedirect(reverse('VideoStoreApp.views.videoUpload'))
            else:
                form = UploadForm()
            return render_to_response('upload.html', {'form':form})
    else:
        return render_to_response('auth.html')
    return render_to_response('auth.html')


def HomePage(request):
    if "session_id" in request.COOKIES.keys():
        s=Sessions.objects.filter(session_id = request.COOKIES.get('session_id'))
        if s.count()> 0:
            video_list = Video.objects.all()
            return render_to_response('VideoStore.html', {'videos': video_list})
        else:
            return render_to_response('auth.html')
    else:
        return render_to_response('auth.html')



def download(request):
    if "session_id" in request.COOKIES.keys():
        s=Sessions.objects.filter(session_id = request.COOKIES.get('session_id'))
        if s.count()> 0:
            try:
                videoName = request.GET.get('video')
                tosend = FileWrapper(file("store/"+videoName))
                res = HttpResponse(tosend, content_type='application/force-download')
                res['Content-Length'] = os.path.getsize("store/"+videoName)
                #res['filename'] = videoName
                render_to_response('VideoStore.html')
                return res
            except:
                return HttpResponseRedirect(reverse('VideoStoreApp.views.HomePage'))
    else:
        return render_to_response('auth.html')

def search(request):
    if "session_id" in request.COOKIES.keys():
        s=Sessions.objects.filter(session_id = request.COOKIES.get('session_id'))
        if s.count()> 0:
            option = request.GET.get('by')
            key = request.GET.get('key')

            if option == "name":
                videolist = Video.objects.filter(name__contains = key)
                return render_to_response('VideoStore.html', {'videos': videolist})
            if option == "category":
                key = request.GET.get('keycat')
                videolist = Video.objects.filter(category = key)
                return render_to_response('VideoStore.html', {'videos': videolist})
            if option == "time":
                if request.GET.get('befaf') == "Before":
                    videolist = Video.objects.filter(timeOfUpload__lte = key)
                    return render_to_response('VideoStore.html', {'videos': videolist})
                if request.GET.get('befaf') == "After":
                    videolist = Video.objects.filter(timeOfUpload__gte = key)
                    return render_to_response('VideoStore.html', {'videos': videolist})
                if request.GET.get('befaf') == "Exact":
                    videolist = Video.objects.filter(timeOfUpload = key)
                    return render_to_response('VideoStore.html', {'videos': videolist})
            if option == "rate":
                key = request.GET.get('score')
                videolist = Video.objects.filter(rating = key)
                return render_to_response('VideoStore.html', {'videos': videolist})
    else:
        return render_to_response('auth.html')


def generate_random_string():
    stringset=string.ascii_letters+string.digits+string.punctuation
    return ''.join([stringset[i%len(stringset)]\
                    for i in [ord(x) for x in os.urandom(10)]])






from django.shortcuts import render, redirect
from .models import Room,Topic, Message
from django.db.models import Q
from django.contrib.auth.models import User
from .forms import RoomForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm

def LoginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or pasword does not exist')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def userprofile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms,'room_message':room_message,'topics':topics}
    return render(request, 'base/profile.html',context)

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error at registretion')
    return render(request, 'base/login_register.html', {'form':form})

def logoutUser(request):
     logout(request)
     return redirect('home')



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.all()
    context = {'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request, 'base/home.html',context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    particepents = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(user=request.user,room=room,  body=request.POST.get('body'))
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room':room,'room_messages':room_messages,'particepents':particepents}
    return render(request, 'base/room.html',context)
# Create your views here.

@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    topics=Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(host=request.user, topic=topic,name=request.POST.get('name'),description=request.POST.get('description'))
        
        return redirect('home')
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     return redirect('home')
    context = {'form':form,'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    context = {'form':form}
    return render(request,'base/update-user.html',context)

@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics=Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Ou are not alloed to do thi')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topics=topic
        room.name=request.POST.get('name')
        room.description=request.POST.get('description')
        return redirect('home')
    context = {'form':form,'topics':topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('Ou are not alloed to do thi')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':room})

@login_required(login_url='/login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('Ou are not alloed to do thi')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':message})
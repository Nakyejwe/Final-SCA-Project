from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Room,Topic,Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def login_page(request):
    page='login'
    if request.user.is_authenticated:
            return redirect('home')
    if request.method == 'POST':        
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'username does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request,'the username and password do not match')
    context={'page':page}
    return render(request,'prog/login_register.html', context)


def logout_page(request):
    logout(request)
    return redirect('home')


def register(request):
    form = UserCreationForm()
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'An Error occured during registration')
    page='register'
    context={'page':page, 'form':form}
    return render(request, 'prog/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q)|
                                Q(name__icontains=q)|
                                Q(description__icontains=q)) 
    room_count = rooms.count()
    topics=Topic.objects.all()
    room_message=Message.objects.filter(Q(room__topic__name__icontains=q))
    context={'rooms':rooms,'topics':topics,'room_count':room_count, 'room_message':room_message}    
    return render(request, 'prog/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages=room.message_set.all()
    participants = room.participants.all()
    if request.method =='POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'))
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context={'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'prog/room.html', context)


def profile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user, 'rooms':rooms,'room_message':room_message, 'topics':topics}
    return render(request, 'prog/profile.html', context)


@login_required(login_url='login')
def create_room(request):
    form =RoomForm()
    if request.method =='POST':
        form = RoomForm(request.POST)
        if form.is_valid:
            room=form.save(commit=False)
            room.host=request.user
            room.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'prog/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('you are not the room owner')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'prog/room_form.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('you are not the room owner')
    if request.method == 'POST':
        room.delete()   
        return redirect('home')
    return render(request, "prog/delete.html", {'obj':room})


@login_required(login_url='login')
def delete_message(request, pk):
    room_message = Message.objects.get(id=pk)
    if request.user != room_message.user:
        return HttpResponse('you are not the room owner')
    if request.method == 'POST':
        room_message.delete()   
        return redirect('home')
    return render(request, "prog/delete.html", {'obj':room_message})


def test(request):
    return render(request, 'prog/test.html')
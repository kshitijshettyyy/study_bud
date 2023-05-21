from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room,Topic,Message
from .forms import RoomForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
# rooms =[
#     {'id':1,'name':'lets learn python'},
#     {'id':2,'name':'css developers'},
#     {'id':3,'name':'lets learn java'},

# overriden in first case
def loginPage(request):
    # if request.user.is_authenicated:
    #     return redirect('home')
    page='login'
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try :
            user=User.objects.get(username=username)
        except:
            messages.error(request,'user does not exist')
        user=authenticate(request,username=username,password=password) 
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username or password does not exist')   
                
        
    context={'page':page}
    return render (request,'base/login_register.html',context)
def logoutUser(request):
    logout(request)
    return redirect('home')
def registerUser(request):
    form=UserCreationForm()
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')
    return render(request,'base/login_register.html',{'form':form})
def home(request):
    sr=request.GET.get('sr') if request.GET.get('sr')!= None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=sr)|
        Q(name__icontains=sr)|
        Q(description__icontains=sr)
        )
     #query set#overriding
    topics=Topic.objects.all()
    room_count=rooms.count()
    room_messages=Message.objects.filter(Q(room__name__icontains=sr))


    context={'rooms':rooms,
             'topics':topics,
             'room_count':room_count,
             'room_messages':room_messages}
    return render(request,'base/home.html',context)
def room(request,pk):
    room=Room.objects.get(id=pk)#query selector
    room_messages=room.message_set.all().order_by('-created')#takes all the messages set to that room
    participants=room.participants.all()
    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context={'room':room,
             'room_messages':room_messages,
             'participants':participants
             }        
    return render(request,'base/room.html',context)
    # return render(request,'room.html')
# def login(request):
#     return HttpResponse('log in here')

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    context={'user':user,
             'rooms':rooms
             }
    return render(request,'base/profile.html',context)


@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/create_room.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)#form is prefilled with the room content of a particular instance
    if request.user!=room.host:
        return HttpResponse('you are not allowed here')
    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}#dictionary
    return render(request,'base/create_room.html',context)#call the form html file 

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room}) 

@login_required(login_url='login')
def deleteMessages(request,pk):
    message=Message.objects.get(id=pk)
    if request.user!=message.user:
        return HttpResponse('You are not allowed here!!!')
    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message}) 


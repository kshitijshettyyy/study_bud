from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room,Topic
from .forms import RoomForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse


# Create your views here.
# rooms =[
#     {'id':1,'name':'lets learn python'},
#     {'id':2,'name':'css developers'},
#     {'id':3,'name':'lets learn java'},

# overriden in first case
def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
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
                
        
    context={}
    return render (request,'base/login_register.html',context)
def logoutUser(request):
    logout(request)
    return redirect('home')

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
    context={'rooms':rooms,'topics':topics,'room_count':room_count}
    return render(request,'base/home.html',context)
def room(request,pk):
    room=Room.objects.get(id=pk)#query selector
    context={'room':room}        
    return render(request,'base/room.html',context)
    # return render(request,'room.html')
# def login(request):
#     return HttpResponse('log in here')
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

from django.shortcuts import render,redirect
from .models import Room
from .forms import RoomForm

# Create your views here.
# rooms =[
#     {'id':1,'name':'lets learn python'},
#     {'id':2,'name':'css developers'},
#     {'id':3,'name':'lets learn java'},

# ]#overriden in first case
def home(request):
    rooms=Room.objects.all() #query set#overriding
    context={'rooms':rooms}
    return render(request,'base/home.html',context)
def room(request,pk):
    room=Room.objects.get(id=pk)#query selector
    context={'room':room}        
    return render(request,'base/room.html',context)
    # return render(request,'room.html')
# def login(request):
#     return HttpResponse('log in here')
def createRoom(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'base/create_room.html',context)
from django.shortcuts import render,redirect
from .models import Room,Topic
from .forms import RoomForm

# Create your views here.
# rooms =[
#     {'id':1,'name':'lets learn python'},
#     {'id':2,'name':'css developers'},
#     {'id':3,'name':'lets learn java'},

# ]#overriden in first case
def home(request):
    sr=request.GET.get('sr') if request.GET.get('sr')!= None else ''

    rooms=Room.objects.filter(topic__name__contains=sr) #query set#overriding
    topics=Topic.objects.all()
    context={'rooms':rooms,'topics':topics}
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


def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)#form is prefilled with the room content of a particular instance
    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}#dictionary
    return render(request,'base/create_room.html',context)#call the form html file 
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

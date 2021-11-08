from django import forms
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm
# rooms = [
#     {'id': 1, 'name': 'Lets learn python'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]


def home(request):
    q = request.GET.get('q') if request.GET.get('q') !=None else ''
    rooms = Room.objects.filter(   # search room by topic, name or description
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        ) 
    # whatever value we have in topic_name at least it contains q(empty string or query para value)
    # if topic__name=q, nothing is going to be filtered because q is empty
    # q=t return both web developmen(t) and javascrip(t)
    # if we don't have query parameter(q=''), all of topic name match that
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST) # pass all the data to RoomForm
        if form.is_valid():
            form.save() # save to database
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # fill up the room with the initial data
    # ignore if statement when we first click Edit in the homepage
    # only executed(if stmt) when we edit and submit                
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room) # instance = room, not to create new room
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

    
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})
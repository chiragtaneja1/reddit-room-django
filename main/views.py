from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Room, Topic, Message
from users.models import User
from .forms import RoomForm, MessageForm

# Create your views here.

# Home
def home(request):
    q = request.GET.get('q') or ''   # getting input from search form 
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) | 
        Q(name__icontains = q) |
        Q(description__icontains = q)
    )                                # filtering result

    # pagination 
    paginator = Paginator(rooms, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    topics_all = Topic.objects.all() # getting all topics
    room_count = rooms.count()       # counting available rooms
    search_room = q                  # storing result input 
    room_messages = Message.objects.filter(Q(room__name__icontains = q)).order_by('-created')[0:7]               # getting message from search input

    context = {'rooms':rooms, 'page_obj': page_obj, 'topics_all':topics_all, 'room_count':room_count, 'search_room':search_room, 'room_messages':room_messages}
    return render(request, 'home.html', context)

# Get Room
def room(request, pk):
    room = Room.objects.get(id=pk)                              # getting room 
    room_messages = room.message_set.all().order_by('-created') # getting all messages of the room
    room_members = room.members.all()                           # getting all members of the room
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.members.add(request.user)                          # adding members to room on post message
        return redirect('room', pk=room.id)

    context = {'room':room, 'room_messages':room_messages, 'room_members':room_members}
    return render(request, 'room.html', context)
    
# Create Room
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()  # getting all topics

    # if request.method == 'POST':
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     return redirect('home')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')                        # getting entered topic name
        topic, created = Topic.objects.get_or_create(name=topic_name) # creating topic if not available
        Room.objects.create(                                          # creating room
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )                                                    
        return redirect('home')

    context = {'form':form, 'object':'Create Room', 'topics':topics}
    return render(request, 'form_room.html', context)

# Update Room
@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk) # getting room 
    form = RoomForm(instance=room)
    topics = Topic.objects.all()  # getting all topics

    if request.user != room.host: # checking room action permission
        return HttpResponse("Forbidden! You don't have a permission to access this page.")

    # if request.method == 'POST':
    #     form = RoomForm(request.POST, instance=room)
    #     if form.is_valid():
    #         form.save() 
    #         return redirect('home')

    if request.method == 'POST':
        topic_name = request.POST.get('topic') # getting entered topic name
        topic, created = Topic.objects.get_or_create(name=topic_name) # creating topic if not available

        room.name = request.POST.get('name') # storing room name
        room.topic = topic                   # storing topic name
        room.description = request.POST.get('description') # storing description name
        room.save()                          # saving room
        return redirect('home')

    context = {'form':form, 'object':'Edit Room', 'topics':topics, 'room':room}
    return render(request, 'form_room.html', context)

# Delete Room
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk) # getting room 

    if request.user != room.host: # checking room action permission
        return HttpResponse("Forbidden! You don't have a permission to access this page.")

    if request.method == 'POST':
        room.delete()            # deleting room
        return redirect('home')

    context = {'object':room}
    return render(request, 'form_delete.html', context)

# Update Message
@login_required(login_url='login')
def updateMessage(request, pk):
    message = Message.objects.get(id=pk) # getting message
    form = MessageForm(instance=message)

    if request.user != message.user: # checking message action permission
        return HttpResponse("Forbidden! You don't have a permission to access this page.")

    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()             # saving message
            return redirect('room', pk=message.room.id)

    context = {'form':form, 'object':'Edit Message'}
    return render(request, 'form_message.html', context)

# Delete Message
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk) # getting message 

    if request.user != message.user: # checking message action permission
        return HttpResponse("Forbidden! You don't have a permission to access this page.")

    if request.method == 'POST':
        message.delete()        # deleting message
        return redirect('room', pk=message.room.id)

    context = {'object':message}
    return render(request, 'form_delete.html', context)

# Get Topics
def allTopics(request):
    q = request.GET.get('q') or ''                       # getting input from search form 
    topics_all = Topic.objects.filter(name__icontains=q) # filtering result 
    search_topic = q                                     # storing result input 
    context = {'topics_all':topics_all, 'search_topic':search_topic}
    return render(request, 'all_topics.html', context)
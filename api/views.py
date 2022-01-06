from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from main.models import Room, Topic
from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):

    routes = [
        'GET    /api/',
        'GET    /api/get-rooms/',
        'GET    /api/get-rooms/:id/',
        'POST   /api/create-rooms/',
        'PUT    /api/edit-rooms/:id/',
        'DELETE /api/edit-rooms/:id/',
        'GET    /api/get-token/',
        'GET    /api/get-token/refresh/',
    ]

    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, id):
    try:
        room = Room.objects.get(pk=id)
    except Room.DoesNotExist:
        context = {'message':'Not Found!', 'status':'404'}
        return Response(context, status=status.HTTP_404_NOT_FOUND)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createRoom(request):
    topic_name = request.POST.get('topic')                
    topic, created = Topic.objects.get_or_create(name=topic_name) 

    room = Room.objects.create(                                        
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
    )  
    room.save()
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)

@api_view(['PUT','DELETE'])
@permission_classes([IsAuthenticated])
def editRoom(request, id):
    try:
        room = Room.objects.get(pk=id)
    except Room.DoesNotExist:
        context = {'message':'Not Found!', 'status':'404'}
        return Response(context, status=status.HTTP_404_NOT_FOUND)

    if request.user != room.host: 
        context = {'message':"Forbidden! You don't have a permission to access this page.", 'status':'403'}
        return Response(context, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        topic_name = request.POST.get('topic') 
        topic, created = Topic.objects.get_or_create(name=topic_name) 

        room.name = request.POST.get('name') 
        room.topic = topic                  
        room.description = request.POST.get('description') 
        room.save()
        serializer = RoomSerializer(room, many=False)
        return Response(serializer.data)
    
    if request.method == 'DELETE':
        room.delete()
        context = {'message':"Deleted Successfully!", 'status':'200'}
        return Response(context, status=status.HTTP_200_OK)
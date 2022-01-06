from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from main.models import Room, Topic
from users.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_active', 'name', 'email', 'bio', 'avatar']

class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class RoomSerializer(ModelSerializer):
    host = UserSerializer(many=False)
    topic = TopicSerializer(many=False)
    members = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = '__all__'

    def get_members(self,obj):
        members = obj.members.all()
        serializer = UserSerializer(members, many=True)
        # return serializer.data
        return [serializer.data[i]['username'] for i in range(len(serializer.data))]
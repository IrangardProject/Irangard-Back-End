from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

from accounts.models import User
from .models import Chat, MessageRoom, Message, UserInRoom


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class MessageRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageRoom
        exclude = ('owner', )

    def create(self, validated_data):
        obj = super(MessageRoomSerializer, self).create(validated_data)
        obj.owner = self.context['request'].user
        obj.save()
        return obj

class MessageSerializer(serializers.ModelSerializer):
    class Meta :
        model = Message
        fields = '__all__'


class UserInRoomSerializer(serializers.ModelSerializer):
    class Meta :
        model = UserInRoom
        fields = '__all__'

class RoomDoesExistInputTemplate(serializers.Serializer):
    user_one = serializers.IntegerField()
    user_two = serializers.IntegerField()

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if not User.objects.filter(id=data['user_one']).exists():
            raise serializers.ValidationError("user one does not exists !")
        if not User.objects.filter(id=data['user_two']).exists():
            raise serializers.ValidationError("user two does not exists !")
        return super(RoomDoesExistInputTemplate, self).validate(data)
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
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

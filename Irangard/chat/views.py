from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework import generics
from accounts.models import User
from accounts.serializers.user_serializers import UserProfileSerializer
from .models import Chat, Message, MessageRoom, UserInRoom
from .permissions import IsRoomMember
from .serializers import ChatSerializer, MessageSerializer, MessageRoomSerializer, UserInRoomSerializer, \
    RoomDoesExistInputTemplate


class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = IsAuthenticated

    @action(
        detail=False,
        methods=['get', 'post'],
        url_path=r'index',
        url_name='chat_index',
        permission_classes=[AllowAny]
    )
    def index(self, request):

        return render(request, 'chat/index.html')

    @action(
        detail=True,
        methods=['get', 'post'],
        url_path=r'room/(?P<room_name>\w+)/username/(?P<username>\w+)',
        url_name='chat_room',
        permission_classes=[AllowAny]
    )
    def room(self, request, room_name, username):

        messages = Chat.objects.filter(room=room_name)

        return render(request, 'chat/room.html', {'room_name': room_name, 'username': username, 'messages': messages})
    
    @action(
        detail=False,
        methods=['get', 'post'],
        url_path=r'room/messages/(?P<room_name>\w+)',
        url_name='chat_room',
        permission_classes=[AllowAny]
    )
    def get_room_messages(self, request, room_name, *args, **kwargs):
        
        try:
            chats = Chat.objects.filter(room_name=room_name)
            serializer = ChatSerializer(chats, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


def room(request, room_name, username):
    messages = Chat.objects.filter(room_name=room_name)
    return render(request, 'chat/room.html', {'room_name': room_name, 'username': username, 'messages': messages})


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]


class MessageRoomViewSet(ModelViewSet):
    queryset = MessageRoom.objects.all()
    serializer_class = MessageRoomSerializer
    permission_classes = [IsAuthenticated]


class AddUserToRoomAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, room_id, format=None):
        room = MessageRoom.objects.filter(id=room_id)
        user = User.objects.filter(id=user_id)
        print(user)
        if not user.exists():
            return Response({'user does not exist !'}, status.HTTP_400_BAD_REQUEST)
        if not room.exists():
            return Response({'room does not exists !'}, status.HTTP_400_BAD_REQUEST)
        if not room.first().owner:
            return Response({'room with no owner !'}, status.HTTP_400_BAD_REQUEST)
        if not (room.first().owner == self.request.user) and \
                not UserInRoom.objects.filter(room=room.first(), user=self.request.user).exists():
            return Response({'you are not allowed to add user in this room!'}, status.HTTP_400_BAD_REQUEST)
        has_joined_before = UserInRoom.objects.filter(user=user.first(), room=room.first()).exists()
        if has_joined_before:
            return Response({'duplicated user in a room in forbidden !'}, status.HTTP_400_BAD_REQUEST)

        user_in_room = UserInRoom.objects.create(user=user.first(), room=room.first())
        user_in_room.save()
        return Response(UserInRoomSerializer(user_in_room).data, status.HTTP_201_CREATED)



class RoomAllMessages(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsRoomMember]

    def get_queryset(self):
        try:
            room_id = int(self.kwargs.get('pk'))
        except Exception as e:
            print(e)
        if not MessageRoom.objects.filter(id=room_id).exists():
            return Response({'room not found'}, status=status.HTTP_404_NOT_FOUND)
        return Message.objects.filter(reciever_room_id=room_id)

class RoomDoesExistAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        input = RoomDoesExistInputTemplate(data=request.POST)
        if input.is_valid(raise_exception=True):
            one_id = input.data['user_one']
            one_rooms = UserInRoom.objects.filter(user_id=one_id).values('room')
            two_id = input.data['user_two']
            two_rooms = UserInRoom.objects.filter(user_id=two_id).values('room')
            for room in one_rooms:
                if room in two_rooms:
                    this_room_obj = MessageRoom.objects.get(id=room['room'])
                    if this_room_obj.type == 'PV' :
                        return Response({'room-id' : this_room_obj.id})
        return Response({'room-id' : 'null'})
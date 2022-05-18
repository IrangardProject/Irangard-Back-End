from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, SpecialUser
from .serializers.user_serializers import UserProfileSerializer
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from . permissions import IsAdmin
from rest_framework.decorators import action, api_view, permission_classes
from .models import SpecialUser, User


class AdminViewSet(GenericViewSet):
    queryset = User.objects.filter(is_admin=True)

    # @action(detail=False, url_path='upgrade-user',  methods=['POST'], permission_classes=[IsAdmin])
    # def UpgradeUser(self, request):
    #     user = User.objects.get(username = request.user.username)
    #     special_user = SpecialUser.objects.create(user = user)
    #     special_user.save()
    #     return Response(f"user with username {request.user.username} upgraded to special user successfully",status = HTTP_200_OK)

    @action(detail=False, url_path='add-admin', methods=['POST'], permission_classes=[permissions.AllowAny])
    def addAdmin(self, request):
        try:
            user = User.objects.get(username=request.user.username)
            user.is_admin = True
            user.save()
            return Response(f'user with username {request.user.username} added as admin', status=status.HTTP_200_OK)
        except:
            return Response(f'unAuthenticated user', status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, url_path='remove-specialuser', methods=['POST'], permission_classes=[IsAdmin])
    def removeSpecialUser(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            sp_user = SpecialUser.objects.get(user=user)
            sp_user.delete()
            user = User.objects.get(username=request.user.username)
            user.is_special = False
            user.save()
            return Response(f'special user with username {user.username} deleted', status=status.HTTP_200_OK)
        except SpecialUser.DoesNotExist:
            return Response(f'special user with username {user.username} doesn not exist', status=status.HTTP_400_BAD_REQUEST)

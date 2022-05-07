from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User , SpecialUser
from .serializers.user_serializers import UserProfileSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from . permissions import IsAdmin
from rest_framework.decorators import action, api_view, permission_classes


class AdminViewSet(GenericViewSet):
    queryset = User.objects.filter(is_admin=True)
    
    @action(detail=False, url_path='upgrade-user',  methods=['POST'], permission_classes=[IsAdmin])
    def UpgradeUser(self, request):
        user = User.objects.get(username = request.user.username)
        special_user = SpecialUser.objects.create(user = user)
        special_user.save()
        return Response(f"user with username {request.user.username} upgraded to special user successfully",status = HTTP_200_OK)
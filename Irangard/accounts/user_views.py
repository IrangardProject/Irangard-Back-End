from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers.user_serializers import UserProfileSerializer
from rest_framework import status

class UserProfile(APIView):
    # serializer_class = UserProfileSerializer
    
    def get(self, request, id, *args, **kwargs):
        
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, id, *args, **kwargs):
        user = User.objects.get(pk=id)
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    

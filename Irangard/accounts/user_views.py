from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers.user_serializers import UserProfileSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

class UserProfile(APIView): 
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    
    def get(self, request, username, *args, **kwargs):
        # permission_classes = [IsAuthenticated]
        parser_classes = [MultiPartParser, FormParser]
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, username, *args, **kwargs):
        permission_classes = [IsAuthenticated]
        parser_classes = [MultiPartParser, FormParser]
        user = User.objects.get(username=username)
        serializer = UserProfileSerializer(user, data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
                
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers.user_serializers import UserProfileSerializer, UserFeedSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action

class UserProfile(APIView): 
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, username, *args, **kwargs):
        parser_classes = [MultiPartParser, FormParser]
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserProfileSerializer(user, context = {'user': request.user})
        return Response(serializer.data)
    
    def put(self, request, username, *args, **kwargs):
        parser_classes = [MultiPartParser, FormParser]
        user = User.objects.get(username=username)
        serializer = UserProfileSerializer(user, data=request.data, context = {'user': request.user})
        if serializer.is_valid():
            serializer.save()
                
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, permission_classes=[AllowAny],
			url_name="get-followers", url_path="followers")
    def get_followers(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = Userf(user.followers, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

        
    

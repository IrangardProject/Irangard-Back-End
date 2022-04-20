from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers.user_serializers import UserProfileSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

class UserProfile(APIView):
    # serializer_class = UserProfileSerializer
    
    def get(self, request, id, *args, **kwargs):
        permission_classes = [IsAuthenticated]
        parser_classes = [MultiPartParser, FormParser]
        
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, id, *args, **kwargs):
        user = User.objects.get(pk=id)
        serializer = UserProfileSerializer(user, data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            fullname_parts = request.data['full_name'].split(' ')
            first_name = fullname_parts[0]
            if len(fullname_parts) > 1:
                last_name = fullname_parts[1]
                for i in range(2, len(fullname_parts)):
                    last_name += ' ' + fullname_parts[i]

                User.objects.filter(pk=id).update(first_name=first_name, last_name=last_name)
                
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    

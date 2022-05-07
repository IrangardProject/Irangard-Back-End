from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

class Pay(APIView):
    
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        
        return Response(f"sent webhook info is :{request.data} ",status=status.HTTP_200_OK)
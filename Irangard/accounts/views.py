from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

class Pay(APIView):
    
    permission_classes = [permission.AllowAny]

    def post(self, request):
        
        return Response("sent webhook info is : ",request.data)
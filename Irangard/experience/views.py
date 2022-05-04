from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import ExperienceSerializer
from .models import Experience
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response


class ExperienceViewSet(ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, username, *args, **kwargs):
    
        parser_classes = [MultiPartParser, FormParser]
        serializer = ExperienceSerializer(context = {'user': request.user})
        return Response(serializer.data)
    
    

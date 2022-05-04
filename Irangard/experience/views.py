from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import ExperienceSerializer, ExperienceListSerializer
from .models import Experience
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response


class ExperienceViewSet(ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def retrieve(self, request, pk=None):
        experience = Experience.objects.get(pk=pk)
        serializer = ExperienceSerializer(experience, context = {'user': request.user})
        return Response(serializer.data)
    
    def list(self, request):
        experiences = Experience.objects.all()
        serializer = ExperienceListSerializer(experiences, context = {'user': request.user}, many=True)
        return Response(serializer.data)
    
    

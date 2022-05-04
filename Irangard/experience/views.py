from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import ExperienceSerializer
from .models import Experience


class ExperienceViewSet(ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    

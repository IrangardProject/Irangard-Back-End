from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .pagination import ExperiencePagination
from .serializers import ExperienceSerializer
from .models import Experience
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.contrib.auth.models import User, AnonymousUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class ExperienceViewSet(ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ExperiencePagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['date_created', 'like_number']
    filterset_fields = ['place__title']
    search_fields = ['title', 'body']
    
    def retrieve(self, request, pk=None):
        # Add field is_owner for retrieve method
        experience = Experience.objects.get(pk=pk)
        serializer = ExperienceSerializer(experience)
        # Check if user is anonymous or not
        if request.user.is_anonymous == False:
            # Get request user, username
            request_user = request.user.username
            request_user.replace(' ', '')
            # Get xp writer usernamme
            xp_user = serializer.data["user_username"]
            xp_user = xp_user.replace(' ', '')
            print(serializer.data["user_username"])
            # Check if xp writer and request user are the same or not
            if request_user == xp_user:
                new_response = {"is_owner":True}    
            else:
                new_response = {"is_owner":False}
        else:
            print(serializer.data["user_username"])
            new_response = {"is_owner":False}
        new_response.update(serializer.data)
        return Response(new_response)
    
    
    

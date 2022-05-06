from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .pagination import ExperiencePagination
from .serializers import ExperienceSerializer
from .models import Experience, Like
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.contrib.auth.models import User, AnonymousUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import GenericAPIView
from rest_framework import status


class ExperienceViewSet(ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ExperiencePagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['date_created', 'like_number']
    filterset_fields = ['place__title', 'place__contact__city', 'place__contact__province']
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
    
 
# class LikeViewSet(GenericAPIView):
#     queryset = Like.objects.all()
#     serializer_class = ExperienceSerializer
#     # permission_classes = [IsAuthenticated]   
    
#     def post(self, request, id, *args, **kwargs):
#         user = request.user
#         experience = Experience.objects.get(pk=id)
#         experience.like_number += 1
#         serializer = ExperienceSerializer(experience, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response("Succesfull", status=status.HTTP_200_OK)
#         else:
#             print(experience.like_number)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    

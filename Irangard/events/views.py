from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import DefaultPagination
from .models import Event, Tag, Image
from .serializers import *
from .permissions import *
from .filters import EventFilter


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [EventPermission]
    pagination_class = DefaultPagination
    
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        tags = data.pop('tags', [])
        images = data.pop('images', [])
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        
        for tag in tags:
            Tag.objects.create(event=event, **tag)
            
        for image in images:
            Image.objects.create(event=event, image=image)
            
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    def update(self, request, *args, **kwargs):
        event = self.get_object()
        data = request.data.copy()
        images = data.pop('images', None)
        tags = data.pop('tags', None)

        if images:
            event.images.all().delete()
            for image in images:
                Image.objects.create(event=event, image=image)

        if tags:
            event.tags.all().delete()
            for tag in tags:
                Tag.objects.create(event=event, **tag)

        return super().update(request, *args, **kwargs)

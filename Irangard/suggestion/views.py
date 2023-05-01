from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import TourSuggestion, EventSuggestion, PlaceSuggestion
from .serializers import (TourSuggestionSerializer,
                        EventSuggestionSerializer, 
                        PlaceSuggestionSerializer)
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .permissions import SuggestionPermission
from tours.models import Tour
from accounts.models import User
from django.core.exceptions import ObjectDoesNotExist


class TourSuggstionViewSet(ModelViewSet):
    queryset = TourSuggestion.objects.all()
    serializer_class = TourSuggestionSerializer
    permission_classes = [SuggestionPermission]
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.validated_data
        if data['sender'] == data['receiver']:
            return Response({'error': 'Sender and receiver cannot be the same.'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        
        print(TourSuggestion.objects.all())
        if TourSuggestion.objects.filter(receiver=data['receiver'], sender=data['sender'], tour=data['tour']):
            print(TourSuggestion.objects.filter(receiver=data['receiver'], sender=data['sender'], tour=data['tour']))
            return Response({'error': 'You have been suggested this tour to this user before'}, status=status.HTTP_400_BAD_REQUEST)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    def perform_create(self, serializer):
        serializer.validated_data['sender'] = self.request.user
        instance = serializer.save()
        return instance
    
    
class EventSuggstionViewSet(ModelViewSet):
    queryset = EventSuggestion.objects.all()
    serializer_class = EventSuggestionSerializer


class PlaceSuggstionViewSet(ModelViewSet):
    queryset = PlaceSuggestion.objects.all()
    serializer_class = PlaceSuggestionSerializer

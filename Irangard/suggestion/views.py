from rest_framework.viewsets import ModelViewSet
from .models import TourSuggestion, EventSuggestion, PlaceSuggestion
from .serializers import (TourSuggestionSerializer,
                        EventSuggestionSerializer, 
                        PlaceSuggestionSerializer)
from rest_framework.response import Response
from rest_framework import status
from .permissions import SuggestionPermission


class TourSuggstionViewSet(ModelViewSet):
    queryset = TourSuggestion.objects.all()
    serializer_class = TourSuggestionSerializer
    permission_classes = [SuggestionPermission]
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['sender'] = self.request.user
        data = serializer.validated_data
        if data['sender'] == data['receiver']:
            return Response({'error': 'Sender and receiver cannot be the same.'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        
        if TourSuggestion.objects.filter(receiver=data['receiver'], sender=data['sender'], tour=data['tour']):
            return Response(
                {'error': 'You have been suggested this tour to this user before'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
class EventSuggstionViewSet(ModelViewSet):
    queryset = EventSuggestion.objects.all()
    serializer_class = EventSuggestionSerializer
    permission_classes = [SuggestionPermission]
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['sender'] = self.request.user
        data = serializer.validated_data
        if data['sender'] == data['receiver']:
            return Response({'error': 'Sender and receiver cannot be the same.'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        
        if EventSuggestion.objects.filter(receiver=data['receiver'], sender=data['sender'], event=data['event']):
            return Response(
                {'error': 'You have been suggested this event to this user before'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PlaceSuggstionViewSet(ModelViewSet):
    queryset = PlaceSuggestion.objects.all()
    serializer_class = PlaceSuggestionSerializer
    permission_classes = [SuggestionPermission]
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['sender'] = self.request.user
        data = serializer.validated_data
        if data['sender'] == data['receiver']:
            return Response({'error': 'Sender and receiver cannot be the same.'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        
        if PlaceSuggestion.objects.filter(receiver=data['receiver'], sender=data['sender'], place=data['place']):
            return Response(
                {'error': 'You have been suggested this place to this user before'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

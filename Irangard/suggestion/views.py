from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import TourSuggestion, EventSuggestion, PlaceSuggestion
from .serializers import (TourSuggestionSerializer,
                        EventSuggestionSerializer, 
                        PlaceSuggestionSerializer)


class TourSuggstionViewSet(ModelViewSet):
    queryset = TourSuggestion.objects.all()
    serializer_class = TourSuggestionSerializer
    

class EventSuggstionViewSet(ModelViewSet):
    queryset = EventSuggestion.objects.all()
    serializer_class = EventSuggestionSerializer


class PlaceSuggstionViewSet(ModelViewSet):
    queryset = PlaceSuggestion.objects.all()
    serializer_class = PlaceSuggestionSerializer

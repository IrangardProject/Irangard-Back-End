from rest_framework import generics
from tours.models import Tour
from places.models import Place
from events.models import Event
from tours.serializers import TourSerializer
from events.serializers import EventSerializer
from places.serializers import PlaceSerializer
from rest_framework.response import Response


class PlaceTriviaAPIView(generics.ListAPIView):
    
    def list(self, request, *args, **kwargs):
        province = self.kwargs.get('province')
        city = self.kwargs.get('city')
        tour_queryset = None
        place_queryset = None
        event_queryset = None
        
        if province:
            tour_queryset = Tour.objects.filter(province=province)
            place_queryset = Place.objects.filter(contact__province=province)
            event_queryset = Event.objects.filter(province=province)

        elif city:
            tour_queryset = Tour.objects.filter(city=city)
            place_queryset = Place.objects.filter(contact__city=city)
            event_queryset = Event.objects.filter(city=city)
            
        else:
            tour_queryset = Tour.objects.all()
            place_queryset = Place.objects.all()
            event_queryset = Event.objects.all()
        
        
        tour_serializer = TourSerializer(tour_queryset, many=True, context={'request': request})
        place_serializer = PlaceSerializer(place_queryset, many=True)
        event_serializer = EventSerializer(event_queryset, many=True)

        data = {
            "tours": tour_serializer.data,
            "places": place_serializer.data,
            "events": event_serializer.data
        }
        return Response(data)

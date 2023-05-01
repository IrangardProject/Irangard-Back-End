from rest_framework import serializers
from .models import TourSuggestion, EventSuggestion, PlaceSuggestion


class SuggestionSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')
    receiver_username = serializers.ReadOnlyField(source='receiver.username')
    
    class Meta:
        abstract = True
        extra_kwargs = {'sender': {'read_only': True}}



class EventSuggestionSerializer(SuggestionSerializer):
    event_title = serializers.SerializerMethodField('get_event_title')

    class Meta:
        model = EventSuggestion
        fields = ['id', 'sender', 'receiver', 'event', 'text', 
                'receiver_username', 'event_title']

    def get_event_title(self, event_suggestion):
        return event_suggestion.event.title


class PlaceSuggestionSerializer(SuggestionSerializer):
    place_title = serializers.SerializerMethodField('get_place_title')

    class Meta:
        model = PlaceSuggestion
        fields = ['id', 'sender', 'receiver', 'place', 'text', 
                'receiver_username', 'place_title']

    def get_place_title(self, place_suggestion):
        return place_suggestion.event.title


class TourSuggestionSerializer(SuggestionSerializer):
    tour_title = serializers.SerializerMethodField('get_tour_title')

    class Meta:
        model = TourSuggestion
        fields = ['id', 'sender', 'receiver', 'tour', 'text', 
                'sender_username', 'receiver_username',
                'tour_title']
        extra_kwargs = {'sender': {'read_only': True}}

    def get_tour_title(self, tour_suggestion):
        return tour_suggestion.tour.title

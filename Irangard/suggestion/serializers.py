from rest_framework import serializers
from .models import TourSuggestion, EventSuggestion, PlaceSuggestion
from rest_framework.exceptions import ValidationError


class SuggestionSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')
    receiver_username = serializers.ReadOnlyField(source='receiver.username')
    
    
    class Meta:
        abstract = True


class TourSuggestionSerializer(SuggestionSerializer):
    tour_title = serializers.SerializerMethodField('get_tour_title')


    class Meta:
        model = TourSuggestion
        fields = ['id', 'sender', 'receiver', 'tour', 'text', 
                'sender_username', 'receiver_username',
                'tour_title']
        
        extra_kwargs = {
            'sender': {'read_only': True},
            'receiver': {'required': False},
            'tour': {'required': False}
        }


    def get_tour_title(self, tour_suggestion):
        return tour_suggestion.tour.title
    
    
    def update(self, instance, validated_data):
        if 'receiver' in validated_data:
            raise ValidationError('Receiver cannot be updated.')
        if 'tour' in validated_data:
            raise ValidationError('Tour cannot be updated.')
        return super().update(instance, validated_data)
    

class EventSuggestionSerializer(SuggestionSerializer):
    event_title = serializers.SerializerMethodField('get_event_title')


    class Meta:
        model = EventSuggestion
        fields = ['id', 'sender', 'receiver', 'event', 'text', 
                'receiver_username', 'event_title']
        extra_kwargs = {
            'sender': {'read_only': True},
            'receiver': {'required': False},
            'event': {'required': False}
        }


    def get_event_title(self, event_suggestion):
        return event_suggestion.event.title
    
    
    def update(self, instance, validated_data):
        if 'receiver' in validated_data:
            raise ValidationError('Receiver cannot be updated.')
        if 'event' in validated_data:
            raise ValidationError('Event cannot be updated.')
        return super().update(instance, validated_data)


class PlaceSuggestionSerializer(SuggestionSerializer):
    place_title = serializers.SerializerMethodField('get_place_title')

    class Meta:
        model = PlaceSuggestion
        fields = ['id', 'sender', 'receiver', 'place', 'text', 
                'receiver_username', 'place_title']
        extra_kwargs = {
            'sender': {'read_only': True},
            'receiver': {'required': False},
            'place': {'required': False}
        }


    def get_place_title(self, place_suggestion):
        return place_suggestion.place.title


    def update(self, instance, validated_data):
        if 'receiver' in validated_data:
            raise ValidationError('Receiver cannot be updated.')
        if 'place' in validated_data:
            raise ValidationError('Place cannot be updated.')
        return super().update(instance, validated_data)
    
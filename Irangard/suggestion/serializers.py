from rest_framework import serializers
from .models import TourSuggestion, EventSuggestion, PlaceSuggestion
from accounts.models import User
from tours.models import Tour
from events.models import Event
from places.models import Place


class UserSuggestionSerializer(serializers.ModelSerializer):
    """Serializer for user's username and Id"""
    class Meta:
        model = User
        fields = ['username', 'id']


class TourBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ['title', 'id']


class EventBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'id']


class PlaceBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['title', 'id']


class SuggestionSerializer(serializers.ModelSerializer):
    sender = UserSuggestionSerializer(read_only=True)
    receiver = UserSuggestionSerializer(read_only=True)
    text = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        abstract = True
   

class EventSuggestionSerializer(SuggestionSerializer):
    event = EventBasicInfoSerializer(read_only=True)

    class Meta:
        model = EventSuggestion
        fields = ['id', 'sender', 'receiver', 'event', 'text']

    def create(self, validated_data):
        print(validated_data)
        print(self.context)
        validated_data['experience_id'] = self.context.get("experience")
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)


class PlaceSuggestionSerializer(SuggestionSerializer):
    place = PlaceBasicInfoSerializer(read_only=True)

    class Meta:
        model = PlaceSuggestion
        fields = ['id', 'sender', 'receiver', 'place', 'text']


class TourSuggestionSerializer(serializers.ModelSerializer):
    sender = UserSuggestionSerializer(read_only=True)
    receiver = UserSuggestionSerializer(read_only=True)
    tour = TourBasicInfoSerializer(read_only=True)

    class Meta:
        model = TourSuggestion
        fields = ('sender', 'receiver', 'tour', 'text')

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)

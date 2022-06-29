from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from .models import *
from accounts.models import User
from datetime import date, datetime, time, timedelta


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['image', 'upload_date']
        read_only_fields = ['upload_date']
        extra_kwargs = {'place': {'write_only': True}}

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['place', 'name']
        extra_kwargs = {'place': {'write_only': True}}

class HoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hours
        fields = ['id', 'weekday', 'start_time', 'end_time', 'all_day']

class ContactSerializer(serializers.ModelSerializer):
    working_hours = HoursSerializer(many=True, read_only=True)
    class Meta:
        model = Contact
        fields = '__all__'
        extra_kwargs = {'place': {'write_only': True}}

class FeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feature
        fields = ['place', 'title']
        extra_kwargs = {'place': {'write_only': True}}

class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['place', 'room_type', 'capacity', 'price']
        extra_kwargs = {'place': {'write_only': True}}

class OptionalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Optional
        fields = ['place', 'title', 'description', 'price']
        extra_kwargs = {'place': {'write_only': True}}

class PlaceSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    contact = ContactSerializer(read_only=True) #read_only=True

    features = FeatureSerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    optional_costs = OptionalSerializer(many=True, read_only=True) #required=False

    class Meta:
        model = Place
        fields = ['id', 'title', 'place_type', 'description', 
        'rate', 'rate_no', 'contact', 'images', 'tags', 
        'is_free', 'features', 'rooms', 'optional_costs']
        read_only_fields = ['id', 'rate', 'rate_no']

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['added_by'] = request.user
        return super().create(validated_data)


# class ResidenceSerializer(PlaceSerializer):
#     features = FeatureSerializer(many=True, read_only=True)
#     rooms = TagSerializer(many=True, read_only=True)

# class RecreationSerializer(PlaceSerializer):
#     optional_costs = OptionalSerializer(many=True, read_only=True)

#     class Meta(PlaceSerializer.Meta):
#         fields = fields + ['is_free']

# class AttractionSerializer(PlaceSerializer):
#     optional_costs = OptionalSerializer(many=True, read_only=True)

#     class Meta(PlaceSerializer.Meta):
#         fields = fields + ['is_free']

 
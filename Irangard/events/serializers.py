from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from .models import Image, Event, Tag
from accounts.models import User
from accounts.serializers.user_serializers import UserSerializer


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

        
class EventSerializer(serializers.ModelSerializer):
    
    images = ImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        fields = [
            'id', 'title', 'event_type', 'event_category',
            'organizer', 'description', 'x_location',
            'y_location', 'province', 'city', 'start_date',
            'end_date', 'start_time', 'end_time', 'images',
            'tags', 'added_by', 'address', 'is_free'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['added_by'] = request.user
        return super().create(validated_data)

from rest_framework import serializers
from .models import Image, Event, Tag


class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = ['image', 'upload_date']
        read_only_fields = ['upload_date']
        extra_kwargs = {'event': {'write_only': True}}


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ['event', 'name']
        extra_kwargs = {'event': {'write_only': True}}

        
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
            'tags', 'added_by', 'address', 'is_free',
            'website', 'phone'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['added_by'] = request.user
        return super().create(validated_data)

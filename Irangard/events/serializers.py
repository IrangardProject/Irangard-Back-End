from rest_framework import serializers
from .models import Image, Event, Tag
from accounts.serializers.user_serializers import UserImageUserNameSerializer


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        ref_name = 'event image serializer'
        fields = ['image', 'upload_date']
        read_only_fields = ['upload_date']
        extra_kwargs = {'event': {'write_only': True}}


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        ref_name = 'event tag serializer'
        model = Tag
        fields = ['event', 'name']
        extra_kwargs = {'event': {'write_only': True}}

        
class EventSerializer(serializers.ModelSerializer):
    added_by = UserImageUserNameSerializer(read_only=True)
    images = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {
            'status': {'read_only': True},
        }
        
    
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['added_by'] = request.user
        return super().create(validated_data)

    
    def get_images(self, obj):
        request = self.context.get('request')
        image_objects = Image.objects.filter(event_id=obj.id)
        if image_objects.exists():
            return [request.build_absolute_uri(image.image.url) for image in image_objects]
        else:
            return []

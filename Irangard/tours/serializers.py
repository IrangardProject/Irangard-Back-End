from rest_framework import serializers
from tours.models import *
from accounts.serializers.user_serializers import *


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.CharField()

    class Meta:
        model = Transaction
        fields = '__all__'


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
        

class TourRegisteredUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'image']


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        ref_name = 'tour tag serializer'
        model = Tag
        fields = ['tour', 'name']
        extra_kwargs = {'tour': {'write_only': True}}


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        ref_name = 'tour image serializer'
        fields = ['image', 'upload_date']
        read_only_fields = ['upload_date']
        extra_kwargs = {'tour': {'write_only': True}}


class TourSerializer(serializers.ModelSerializer):
    owner = SpecialUserSerializer(read_only=True)
    is_booked = serializers.SerializerMethodField('booked')
    bookers = TourRegisteredUserSerializer(many=True,read_only=True)
    is_expired = serializers.SerializerMethodField()
    images = ImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Tour
        fields = '__all__'
        extra_fields = ('is_booked')
        extra_kwargs = {
            'status': {'read_only': True},
        }
    
    def create(self, validated_data):
        validated_data['owner_id'] = self.context.get("owner")
        return super().create(validated_data)

    def booked(self, tour):
        request = self.context.get("request")
        return tour.booked(request.user)

    def get_is_expired(self, obj):
        return obj.is_expired

from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
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


class TourSerializer(serializers.ModelSerializer):
    owner = SpecialUserSerializer(read_only=True)
    is_booked = serializers.SerializerMethodField('booked')
    class Meta:
        model = Tour
        fields = '__all__'
        extra_fields = ('is_booked')

    def create(self, validated_data):
        validated_data['owner_id'] = self.context.get("owner")
        return super().create(validated_data)
    
    def booked(self, tour):
        request = self.context.get("request")
        return tour.booked(request.user)
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from tours.models import *


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
    class Meta:
        model = Tour
        fields = '__all__'
    